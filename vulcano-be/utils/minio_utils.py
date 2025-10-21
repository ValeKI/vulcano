import os
from minio import Minio
from config import CURRENT_CONFIG
from io import BytesIO

class MinioUtils:
    def get_minio_client(self):
        print("[MINIO] Creating Minio client")
        return Minio(
            CURRENT_CONFIG.MINIO_ENDPOINT,
            access_key=CURRENT_CONFIG.MINIO_ACCESS_KEY,
            secret_key=CURRENT_CONFIG.MINIO_SECRET_KEY,
            secure=CURRENT_CONFIG.MINIO_SECURE
        )

    def ensure_bucket_exists(self):
        print("[MINIO] Ensuring bucket exists")
        client = self.get_minio_client()
        bucket = CURRENT_CONFIG.MINIO_BUCKET
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            print(f"[MINIO] Bucket created: {bucket}")
        else:
            print(f"[MINIO] Bucket already exists: {bucket}")

    def create_user_subfolders(self, user_id):
        print(f"[MINIO] Creating subfolders for user_id={user_id}")
        self.ensure_bucket_exists()
        client = self.get_minio_client()
        bucket = CURRENT_CONFIG.MINIO_BUCKET
        folders = [
            f"user/{user_id}/files/",
            f"user/{user_id}/questions/",
            f"user/{user_id}/answers/"
        ]
        for folder in folders:
            # MinIO non ha vere cartelle, si crea un oggetto "vuoto" con nome che termina con /
            client.put_object(bucket, folder, data=b"", length=0)
            print(f"[MINIO] Subfolder created: {folder}")

    def upload_user_file(self, user_id, file_name, file_data):
        print(f"[MINIO] Uploading file: user_id={user_id}, file_name={file_name}")
        self.ensure_bucket_exists()
        client = self.get_minio_client()
        bucket = CURRENT_CONFIG.MINIO_BUCKET
        object_name = f"user/{user_id}/files/{file_name}"
        # Usa BytesIO per fornire un oggetto file-like
        file_obj = BytesIO(file_data)
        file_obj.seek(0, os.SEEK_END)
        length = file_obj.tell()
        file_obj.seek(0)
        client.put_object(
            bucket,
            object_name,
            data=file_obj,
            length=length
        )
        print(f"[MINIO] File uploaded: {object_name}")

    def get_user_file(self, user_id, file_name):
        print(f"[MINIO] Getting file: user_id={user_id}, file_name={file_name}")
        self.ensure_bucket_exists()
        client = self.get_minio_client()
        bucket = CURRENT_CONFIG.MINIO_BUCKET
        object_name = f"user/{user_id}/files/{file_name}"
        response = client.get_object(bucket, object_name)
        print(f"[MINIO] File retrieved: {object_name}")
        return response.read()
