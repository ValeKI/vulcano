#!/bin/sh
sleep 5
echo "Creating buckets in MinIO..."
mc alias set vulcano-minio http://minio:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"

echo "Creating bucket: vulcano-minio"
mc mb vulcano-minio

echo "Buckets created successfully."
exit 0
