import cv2
import numpy as np

import cv2
import numpy as np

def burnt_score(image_path: str,
                threshold: int = 240,
                weight: float = 1.2) -> float:

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Image not loaded: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    bright_ratio = np.mean(gray >= threshold)
    score = np.clip(bright_ratio * weight, 0, 1)

    return float(score)
# בדיקה על תמונה אחת

image = cv2.imread(r"C:\Users\weingertenb\Desktop\Chaplin_The_Kid.jpg")

if image is None:
    raise Exception("image not loaded")

score = burnt_score(image)

print("Burn score:", score)

r"""
print("-----------a fuw images:----------")
# בדיקה על כמה תמונות

import cv2

paths = [
    r"C:\\Users\weingertenb\Desktop\Chaplin_The_Kid.jpg",
    r"C:\\Users\weingertenb\Desktop\Chaplin_The_Kid2.jpg",
    r"C:\\Users\weingertenb\Desktop\Chaplin_The_Kid3.jpg",
    r"C:\\Users\weingertenb\Desktop\yoav_0004.JPG"
]

for path in paths:
    img = cv2.imread(path)
    if img is None:
        continue

    score = burnt_score(img)
    print(path, "->", score)
burnt_score(image, threshold=230, weight=1.5)
"""