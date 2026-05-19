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