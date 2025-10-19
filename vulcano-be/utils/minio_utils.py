import os
from minio import Minio
from config import CURRENT_CONFIG

def get_minio_client():
    return Minio(
        CURRENT_CONFIG.MINIO_ENDPOINT,
        access_key=CURRENT_CONFIG.MINIO_ACCESS_KEY,
        secret_key=CURRENT_CONFIG.MINIO_SECRET_KEY,
        secure=CURRENT_CONFIG.MINIO_SECURE
    )

def create_user_subfolders(user_id):
    client = get_minio_client()
    bucket = CURRENT_CONFIG.MINIO_BUCKET
    folders = [
        f"user/{user_id}/files/",
        f"user/{user_id}/questions/",
        f"user/{user_id}/answers/"
    ]
    for folder in folders:
        # MinIO non ha vere cartelle, si crea un oggetto "vuoto" con nome che termina con /
        client.put_object(bucket, folder, data=b"", length=0)

def upload_user_file(user_id, file_name, file_data):
    client = get_minio_client()
    bucket = CURRENT_CONFIG.MINIO_BUCKET
    object_name = f"user/{user_id}/files/{file_name}"
    client.put_object(
        bucket,
        object_name,
        data=file_data,
        length=len(file_data)
    )

def get_user_file(user_id, file_name):
    client = get_minio_client()
    bucket = CURRENT_CONFIG.MINIO_BUCKET
    object_name = f"user/{user_id}/files/{file_name}"
    response = client.get_object(bucket, object_name)
    return response.read()
