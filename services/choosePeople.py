

import os
from PIL import Image
import imagehash
from collections import defaultdict
from services.scoring import get_image_score
from services.burnt import burnt_score
from services.sharpness import calculate_sharpness_laplacian

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

print("------------main----------------")

def best_image_per_person(
    images_folder,
    score_func,
    threshold=0.5
):

    supported = (".jpg", ".jpeg", ".png", ".webp")

    groups = []  # כל קבוצה = אדם אחד

    for file in os.listdir(images_folder):

        if not file.lower().endswith(supported):
            continue

        path = os.path.join(images_folder, file)

        encoding = get_face_encoding(path)

        if encoding is None:
            continue

        score = score_func(path)

        matched = False

        for group in groups:

            dist = np.linalg.norm(encoding - group["rep"])

            if dist < threshold:

                group["images"].append({
                    "path": path,
                    "encoding": encoding,
                    "score": score
                })

                matched = True
                break

        if not matched:

            groups.append({
                "rep": encoding,
                "images": [{
                    "path": path,
                    "encoding": encoding,
                    "score": score
                }]
            })

    # לבחור תמונה הכי טובה מכל אדם
    result = []

    for group in groups:

        best = max(group["images"], key=lambda x: x["score"])

        result.append(best["path"])

    return result