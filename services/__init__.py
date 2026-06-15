import os
import cv2

path = r"O:\share\project miri and brachy\chassid\out\yoav_0001 - עותק.JPG"

print(os.path.exists(path))

img = cv2.imread(path)

print(img is None)