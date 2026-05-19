import boto3
from services.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET_NAME

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def upload_to_s3(file_path, s3_key):
    s3.upload_file(file_path, S3_BUCKET_NAME, s3_key)
    return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"