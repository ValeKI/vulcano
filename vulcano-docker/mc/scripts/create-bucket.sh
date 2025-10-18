#!/bin/sh
sleep 5
echo "Creating buckets in MinIO..."
mc alias set vulcano-minio http://minio:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"

# to manage pdf files
echo "Creating bucket: user/files"
mc mb vulcano-minio/user/files
echo "Bucket created: user/files"

# to save questions
echo "Creating bucket: user/questions"
mc mb vulcano-minio/user/questions
echo "Bucket created: user/questions"

# to save answers
echo "Creating bucket: user/answers"
mc mb vulcano-minio/user/answers
echo "Bucket created: user/answers"

echo "Buckets created successfully."
exit 0
