FROM quay.io/minio/mc:RELEASE.2025-08-13T08-35-41Z

# Copia lo script di creazione bucket
COPY /scripts/create-bucket.sh /usr/bin/create-bucket.sh
RUN chmod +x /usr/bin/create-bucket.sh

ENTRYPOINT ["/usr/bin/create-bucket.sh"]