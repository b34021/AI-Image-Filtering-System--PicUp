import os
import asyncio
import shutil
from dto.EventDTO import EventDTO
from repository.event_repository import EventRepository
from services.face_utils import extract_single_faces
from services.remove_duplicate import remove_duplicate_faces
from services.deduplicate import DeduplicateService
from services.scoring import get_image_score
from services.ml_classifier import predict_image_category
from repository.people_repository import people_repository
from services.rename_images import clean_filename
from services.image_io import safe_imread


SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

# מיפוי מפלט ה-ML Classifier לשמות תיקיות האלבום
# ה-ML מחזיר: bride_chair, chuppa, dance, meal, out, yichud
# תיקיות האלבום: bride_chair, chuppa, dance, meal, outdoor, yichud, mitzva_tantz
# מיפוי מפלט ה-ML Classifier (10 classes) לשמות תיקיות האלבום (8 folders)
# ML מחזיר: bride_chair, chuppa, dance_men, dance_women, inside,
#            meal_men, meal_women, mizva_tanz, out, yichud
# תיקיות אלבום: bride_chair, chuppa, dance, inside, meal,
#                mitzva_tantz, outdoor, yichud
CATEGORY_MAP = {
    "out": "outdoor",
    "general": "outdoor",
    "dance_men": "dance",
    "dance_women": "dance",
    "meal_men": "meal",
    "meal_women": "meal",
    "inside": "inside",
    "mizva_tanz": "mitzva_tantz",
    # bride_chair, chuppa, yichud — עוברים כמו שהם
}

# מיפוי קטגוריות ML → קטגוריות עבור scoring (לצורך בונוסים)
SCORING_CATEGORY_MAP = {
    "dance_men": "dance",
    "dance_women": "dance",
    "meal_men": "meal",
    "meal_women": "meal",
    "mizva_tanz": "mitzva_tantz",
}

# מיפוי קטגוריות ML → מגדר (עבור meal ו-dance)
GENDER_FROM_CATEGORY = {
    "dance_men": "men",
    "dance_women": "women",
    "meal_men": "men",
    "meal_women": "women",
}

VALID_CATEGORIES = {
    "bride_chair", "chuppa", "dance", "meal",
    "outdoor", "inside", "yichud", "mitzva_tantz",
}


class EventService:
    def __init__(self):
        self.repo = EventRepository()
        self.deduplicate_service = DeduplicateService()

    async def get_faces(self, event_data: EventDTO):
        faces = extract_single_faces(event_data.pathToFolder)
        faces = remove_duplicate_faces(faces)
        return faces

    async def create_event(self, event_data: EventDTO):
        """Save event to DB (legacy)."""
        return await self.repo.create_event(event_data)

    async def build_album(self, event_data: EventDTO) -> dict:
        """
        Full pipeline:
        1. Dedup — move low-quality duplicates to Junk/
        2. Score all remaining images
        3. Distribute into category folders under album/
        """
        folder = event_data.pathToFolder
        print(f"[build_album] START folder={folder}")

        if len(event_data.categories) != 8:
            raise ValueError("Exactly 8 categories required")

        # ── שלב 1: הסרת כפילויות ──────────────────────────
        print("[build_album] Phase 1: dedup...")
        dedup_result = await asyncio.to_thread(
            self.deduplicate_service.remove_duplicate_images, folder
        )
        print(f"[build_album] dedup done: {dedup_result}")

        # ── שלב 2: איסוף תמונות ───────────────────────────
        clean_filename(folder)
        print("[build_album] Phase 2: listing files...")

        try:
            all_files = [
                f for f in os.listdir(folder)
                if f.lower().endswith(SUPPORTED_FORMATS)
                and os.path.isfile(os.path.join(folder, f))
            ]
        except Exception as e:
            raise RuntimeError(f"Failed to list folder: {e}")

        if not all_files:
            return {
                "status": "ok", "dedup": dedup_result,
                "message": "no images to score",
            }

        print(f"[build_album] Found {len(all_files)} images")

        # ── שלב 3: טעינת embeddings ───────────────────────
        print("[build_album] Phase 3: loading embeddings...")
        selected_embeddings = await people_repository.get_selected(
            event_data.clientId, "0"
        )
        bride_embedding = await people_repository.get_bride(
            event_data.clientId, "0"
        )
        groom_embedding = await people_repository.get_groom(
            event_data.clientId, "0"
        )

        # ── שלב 4: ניקוד מקבילי ────────────────────────────
        print("[build_album] Phase 4: scoring...")
        sem = asyncio.Semaphore(int(os.environ.get("PICUP_WORKERS", 2)))
        scored: list[dict] = []

        async def _score_one(name: str) -> dict | None:
            async with sem:
                path = os.path.join(folder, name)
                img = await asyncio.to_thread(safe_imread, path)
                if img is None:
                    return None

                ml = await asyncio.to_thread(
                    predict_image_category, image_path=path, image=img
                )
                raw_cat = ml.get("category", "general")
                # מפה לשמות תיקיות האלבום
                cat = CATEGORY_MAP.get(raw_cat, raw_cat)
                # אם הקטגוריה לא חוקית — התמונה תשלח ל-Junk (לא נכפה outdoor)
                album_category = cat if cat in VALID_CATEGORIES else None

                # מיפוי קטגוריה עבור scoring (איחוד dance_men/dance_women → dance וכו')
                scoring_cat = SCORING_CATEGORY_MAP.get(raw_cat, raw_cat)

                data = await asyncio.to_thread(
                    get_image_score,
                    image_path=path, image=img,
                    selected_embeddings=selected_embeddings,
                    category=scoring_cat,
                    bride_embedding=bride_embedding,
                    groom_embedding=groom_embedding,
                )
                data["image_path"] = path
                data["image_name"] = name
                data["album_category"] = album_category  # None = ילך ל-Junk
                data["raw_category"] = raw_cat  # קטגוריית ML מקורית (לזיהוי מגדר)
                return data

        tasks = [_score_one(name) for name in all_files]
        results = await asyncio.gather(*tasks)
        for r in results:
            if r is not None:
                scored.append(r)

        # ── שלב 5: מיון יורד ────────────────────────────────
        scored.sort(key=lambda x: x["score"], reverse=True)

        # ── שלב 6: הפצה לתיקיות קטגוריות ───────────────────
        quota = {c.category_name: c.selected_count for c in event_data.categories}
        print(f"[build_album] Scored {len(scored)} images")
        print("[build_album] Phase 5: distributing to album...")
        album_root = os.path.join(folder, "album")
        os.makedirs(album_root, exist_ok=True)
        for cat_name in quota:
            os.makedirs(os.path.join(album_root, cat_name), exist_ok=True)

        filled = {c: 0 for c in quota}
        assigned: dict[str, str] = {}
        gender_count = {"meal": {"men": 0, "women": 0}, "dance": {"men": 0, "women": 0}}

        # שלב 6: שיבוץ לפי קטגוריה אמיתית (עד המכסה)
        for item in scored:
            cat = item.get("album_category")
            name = item["image_name"]

            # קטגוריה לא מזוהה — ישלח ל-Junk, לא ננסה לשבץ
            if cat is None:
                continue

            if cat not in quota or filled[cat] >= quota[cat]:
                continue

            if cat in ("meal", "dance"):
                raw = item.get("raw_category", "")
                g = GENDER_FROM_CATEGORY.get(raw, "women")
                if gender_count[cat].get(g, 0) >= quota[cat] / 2:
                    continue
                gender_count[cat][g] = gender_count[cat].get(g, 0) + 1

            shutil.move(item["image_path"], os.path.join(album_root, cat, name))
            filled[cat] += 1
            assigned[name] = cat

        # ── שלב 8: העברת תמונות שלא שובצו אל Junk ─────────
        junk_folder = os.path.join(folder, "Junk")
        os.makedirs(junk_folder, exist_ok=True)
        junk_count = 0
        junk_items: list[dict] = []
        for item in scored:
            name = item["image_name"]
            if name in assigned:
                continue
            src = item["image_path"]
            dst = os.path.join(junk_folder, name)
            if os.path.exists(dst):
                base, ext = os.path.splitext(name)
                dst = os.path.join(junk_folder, f"{base}_junk{ext}")
            shutil.move(src, dst)
            junk_count += 1
            item["image_path"] = dst  # update path for backfill
            junk_items.append(item)

        # ── שלב 9: השלמת חסרים מתוך Junk ──────────────────
        # קודם נסה להתאים לפי קטגוריה, אחרת קח את התמונות עם הציון הגבוה ביותר
        for cat in quota:
            while filled[cat] < quota[cat]:
                best_idx = -1
                best_score = -1.0
                for i, item in enumerate(junk_items):
                    item_cat = item.get("album_category")
                    if item_cat is None:
                        raw = item.get("raw_category", "")
                        item_cat = CATEGORY_MAP.get(raw, raw)
                    if item_cat == cat and item["score"] > best_score:
                        best_score = item["score"]
                        best_idx = i
                # fallback: קח את התמונה עם הציון הגבוה ביותר
                if best_idx == -1 and junk_items:
                    for i, item in enumerate(junk_items):
                        if item["score"] > best_score:
                            best_score = item["score"]
                            best_idx = i
                if best_idx == -1:
                    break
                item = junk_items.pop(best_idx)
                name = item["image_name"]
                shutil.move(item["image_path"], os.path.join(album_root, cat, name))
                filled[cat] += 1
                assigned[name] = cat
                junk_count -= 1

        # ── שלב 10: שמירת האירוע ב-DB עם נתיב האלבום ──────
        print(f"[build_album] Phase 10: saving to DB. junk={junk_count}, filled={filled}")
        event_data.pathToFolder = album_root
        db_event = await self.repo.create_event(event_data)

        return {
            "status": "ok",
            "event": db_event,
            "dedup": dedup_result,
            "total_scored": len(scored),
            "album_folder": album_root,
            "junk_folder": junk_folder,
            "categories_filled": filled,
            "gender_counts": gender_count,
            "junk_count": junk_count,
        }

    async def get_images_recursive(self, folder_path: str) -> list[str]:
        images = []
        if not os.path.isdir(folder_path):
            return images
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in SUPPORTED_FORMATS:
                    full_path = os.path.join(root, file)
                    images.append(full_path)
        return images

    async def get_images_as_base64(self, folder_path: str) -> list[str]:
        """מחזיר רשימת תמונות כ-base64 strings (ללא data:image prefix)."""
        import base64

        result = []
        if not os.path.isdir(folder_path):
            return result

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in SUPPORTED_FORMATS:
                    full_path = os.path.join(root, file)
                    try:
                        data = await asyncio.to_thread(self._read_as_base64, full_path)
                        result.append(data)
                    except Exception:
                        continue
        return result

    @staticmethod
    def _read_as_base64(file_path: str) -> str:
        import base64
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")


    async def list_events(self):
        return await self.repo.get_all_events()

    async def get_event_by_id(self, event_id: int):
        return await self.repo.get_event(event_id)

    async def update_event(self, event_id: str, update_data: dict):
        return await self.repo.update_event(event_id, update_data)

    async def remove_event(self, event_id: str):
        return await self.repo.delete_event(event_id)
