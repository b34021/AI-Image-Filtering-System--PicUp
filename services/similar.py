import imagehash
from PIL import Image

def check_image_similarity(image_path1, image_path2):
    # טוען את התמונות
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # מחולל את ה-hash לכל תמונה
    hash1 = imagehash.average_hash(image1)
    hash2 = imagehash.average_hash(image2)

    # מחשב את המרחק בין ה-hashes
    difference = hash1 - hash2
    return difference

image_path_n1 = r'C:\Users\fisherm\Desktop\b.jpg'
image_path_n2 = r'C:\Users\fisherm\Desktop\unsplash_stock_photos-1024x683.jpg'
similarity = check_image_similarity(image_path_n1, image_path_n2)
print(f"The hash difference between images: {similarity}")
