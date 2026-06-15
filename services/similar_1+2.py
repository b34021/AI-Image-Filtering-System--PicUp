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