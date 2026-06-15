
#1
import os
from PIL import Image
import imagehash
from collections import defaultdict
from services.scoring import get_image_score
# from services.burnt import burnt_score
from services.burnt import Burnt
# from services.sharpness import calculate_sharpness_laplacian
from services.sharpness import Sharpness

def remove_duplicates_fast(images_folder, threshold=5, prefix_len=8):

    supported_formats = (".jpg", ".jpeg", ".png", ".webp")

    buckets = defaultdict(list)

    for filename in os.listdir(images_folder):

        if not filename.lower().endswith(supported_formats):
            continue

        path = os.path.join(images_folder, filename)

        try:
            img = Image.open(path).convert("RGB")
            h = imagehash.phash(img)

        except:
            continue

        bucket_key = str(h)[:prefix_len]

        is_duplicate = False

        for saved in buckets[bucket_key]:
            if abs(h - saved["hash"]) <= threshold:
                is_duplicate = True
                break

        if not is_duplicate:

            score = get_image_score(path)

            buckets[bucket_key].append({
                "filename": filename,
                "path": path,
                "hash": h,
                "score": score
            })

    # בחירת התמונה הכי טובה מכל קבוצה
    result = []

    for bucket in buckets.values():

        best = max(bucket, key=lambda x: x["score"])

        result.append({
            "filename": best["filename"],
            "path": best["path"],
            "score": best["score"]
        })

    return result
# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("START")

    print(__name__)

    folder = r"O:\share\project miri and brachy\chassid\out"

    print("Folder exists:", os.path.exists(folder))

    print(os.listdir(folder))

    result = remove_duplicates_fast(folder)

    print(f"Unique images: {len(result)}")

    for img in result:
        print(img["filename"])
#2
import imagehash
from PIL import Image


def remove_similar_images_from_list(image_paths, hashfunc=imagehash.phash, hash_size=8, max_distance=5):
    """
    מסירה תמונות זהות או כמעט זהות מתוך רשימה.

    :param image_paths: רשימה של נתיבי תמונות
    :param hashfunc: פונקציית hash (default: phash)
    :param hash_size: גודל hash
    :param max_distance: המרחק המקסימלי בין hashes כדי להיחשב כפולות
    :return: רשימה חדשה של תמונות ייחודיות
    """
    unique_hashes = []
    unique_images = []

    for path in image_paths:
        try:
            img = Image.open(path)
            img_hash = hashfunc(img, hash_size=hash_size)

            # בדיקה מול כל ה‑hashes הייחודיים הקיימים
            is_duplicate = False
            for h in unique_hashes:
                if img_hash - h <= max_distance:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_hashes.append(img_hash)
                unique_images.append(path)
        except Exception as e:
            print(f"Error processing {path}: {e}")

    return unique_images


# דוגמה לשימוש
image_list = [
    r"C:\Users\fisherm\Desktop\b.jpg",
    r"C:\Users\fisherm\Desktop\similar_b.jpg",
    r"C:\Users\fisherm\Desktop\unique.jpg"
]

unique_images = remove_similar_images_from_list(image_list, max_distance=5)
print(unique_images)
#1+2
#1-בוחרת תמונות איכותיות ביותר
#2-מסירה כפילויות
#הפונקציה הזאת מסננת ומסירה#
import os
from collections import defaultdict
from PIL import Image
import imagehash

from services.scoring import get_image_score


def remove_duplicates_and_choose_best(images_folder,
                                      threshold=5,
                                      prefix_len=8):

    supported_formats = (".jpg", ".jpeg", ".png", ".webp")

    buckets = defaultdict(list)

    for filename in os.listdir(images_folder):

        if not filename.lower().endswith(supported_formats):
            continue

        path = os.path.join(images_folder, filename)

        try:
            img = Image.open(path).convert("RGB")
            h = imagehash.phash(img)
        except Exception:
            continue

        bucket_key = str(h)[:prefix_len]

        buckets[bucket_key].append({
            "filename": filename,
            "path": path,
            "hash": h
        })

    result = []

    for bucket in buckets.values():

        groups = []

        for item in bucket:

            found_group = None

            for group in groups:
                if abs(item["hash"] - group[0]["hash"]) <= threshold:
                    found_group = group
                    break

            if found_group:
                found_group.append(item)
            else:
                groups.append([item])

        for group in groups:

            best_item = None
            best_score = -1

            for item in group:

                score = get_image_score(item["path"])

                if score > best_score:
                    best_score = score
                    best_item = item

            result.append({
                "filename": best_item["filename"],
                "path": best_item["path"],
                "score": best_score
            })

    return result