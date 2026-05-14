import os
from datetime import datetime
from db import get_collection
from storage import upload_to_s3
from config import LOCAL_IMAGE_DIR, COLLECTION_NAME

collection = get_collection(COLLECTION_NAME)

def upload_image(file_path):
    file_name = os.path.basename(file_path)
    s3_key = f"images/{file_name}"

    s3_url = upload_to_s3(file_path, s3_key)

    metadata = {
        "file_name": file_name,
        "s3_url": s3_url,
        "upload_date": datetime.utcnow(),
        "tags": [],
        "category": None,
        "processed": False
    }
    collection.insert_one(metadata)
    print(f"Uploaded {file_name} -> {s3_url}")

def upload_all_images():
    for file in os.listdir(LOCAL_IMAGE_DIR):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            upload_image(os.path.join(LOCAL_IMAGE_DIR, file))
    print("All images uploaded and metadata saved to MongoDB.")