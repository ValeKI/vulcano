#!/bin/sh
sleep 5
echo "Creating buckets in MinIO..."
mc alias set vulcano-minio http://minio:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"

echo "Creating bucket: user"
mc mb vulcano-minio/user
echo "Bucket created: vulcano-minio/user"

echo "Buckets created successfully."
exit 0
