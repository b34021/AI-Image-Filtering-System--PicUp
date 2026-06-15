import os
from collections import defaultdict

import cv2
import numpy as np
from PIL import Image
import imagehash
from insightface.app import FaceAnalysis

from services.scoring import get_image_score


# =========================================================
# FACE MODEL
# =========================================================

app = FaceAnalysis(
    name="buffalo_l"
)

app.prepare(
    ctx_id=0,        # GPU
    det_size=(640, 640)
)


# =========================================================
# FACE EMBEDDING
# =========================================================

def get_face_embedding(path):

    img = cv2.imread(path)

    if img is None:
        return None

    faces = app.get(img)

    if len(faces) == 0:
        return None

    # בוחר את הפנים הגדולות ביותר
    face = max(
        faces,
        key=lambda f:
        (f.bbox[2] - f.bbox[0]) *
        (f.bbox[3] - f.bbox[1])
    )

    return face.embedding


# =========================================================
# DUPLICATE REMOVAL
# =========================================================

def remove_duplicates_fast(
    images_folder,
    hash_threshold=5,
    prefix_len=8
):

    supported_formats = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    )

    buckets = defaultdict(list)

    for filename in os.listdir(images_folder):

        if not filename.lower().endswith(supported_formats):
            continue

        path = os.path.join(images_folder, filename)

        try:

            img = Image.open(path).convert("RGB")

            phash = imagehash.phash(img)

        except Exception:
            continue

        bucket_key = str(phash)[:prefix_len]

        duplicate_found = False

        for saved in buckets[bucket_key]:

            dist = abs(phash - saved["hash"])

            if dist <= hash_threshold:

                duplicate_found = True

                # שמירת התמונה הטובה יותר
                new_score = get_image_score(path)

                if new_score > saved["score"]:

                    saved["filename"] = filename
                    saved["path"] = path
                    saved["hash"] = phash
                    saved["score"] = new_score

                break

        if not duplicate_found:

            score = get_image_score(path)

            buckets[bucket_key].append({
                "filename": filename,
                "path": path,
                "hash": phash,
                "score": score
            })

    result = []

    for bucket in buckets.values():

        for item in bucket:

            result.append(item)

    return result


# =========================================================
# PERSON CLUSTERING
# =========================================================

def best_image_per_person(
    images_folder,
    selected_embeddings=None,
    face_threshold=0.6
):

    supported_formats = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    )

    groups = []

    for filename in os.listdir(images_folder):

        if not filename.lower().endswith(supported_formats):
            continue

        path = os.path.join(images_folder, filename)

        # -------------------------------------------------
        # FACE EMBEDDING
        # -------------------------------------------------

        embedding = get_face_embedding(path)

        if embedding is None:
            continue

        # -------------------------------------------------
        # IMAGE QUALITY SCORE
        # -------------------------------------------------

        score = get_image_score(path)

        matched = False

        # -------------------------------------------------
        # COMPARE TO EXISTING GROUPS
        # -------------------------------------------------

        for group in groups:

            dist = np.linalg.norm(
                embedding - group["rep"]
            )

            if dist < face_threshold:

                group["images"].append({
                    "filename": filename,
                    "path": path,
                    "embedding": embedding,
                    "score": score
                })

                matched = True

                break

        # -------------------------------------------------
        # CREATE NEW GROUP
        # -------------------------------------------------

        if not matched:

            groups.append({

                "rep": embedding,

                "images": [{
                    "filename": filename,
                    "path": path,
                    "embedding": embedding,
                    "score": score
                }]
            })

    # =====================================================
    # BEST IMAGE PER PERSON
    # =====================================================

    result = []

    for group in groups:

        best = max(
            group["images"],
            key=lambda x: x["score"]
        )

        result.append({
            "filename": best["filename"],
            "path": best["path"],
            "score": best["score"]
        })

    return result


# =========================================================
# FULL PIPELINE
# =========================================================

def process_event_album(folder):

    print("STEP 1 - REMOVE DUPLICATES")

    unique_images = remove_duplicates_fast(folder)

    temp_folder = "__temp_unique__"

    os.makedirs(temp_folder, exist_ok=True)

    # יצירת תיקיית עבודה זמנית
    for img in unique_images:

        filename = img["filename"]

        src = img["path"]

        dst = os.path.join(temp_folder, filename)

        if not os.path.exists(dst):

            image = Image.open(src)

            image.save(dst)

    print("STEP 2 - BEST IMAGE PER PERSON")

    result = best_image_per_person(temp_folder)

    return result


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    folder = r"O:\share\project miri and brachy\chassid\out"

    results = process_event_album(folder)

    print("\nFINAL RESULTS:\n")

    for item in results:

        print(
            item["filename"],
            "->",
            round(item["score"], 2)
        )