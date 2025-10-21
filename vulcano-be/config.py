import os
from dotenv import load_dotenv
from pathlib import Path

env = os.getenv("FLASK_ENV", "local")
dotenv_path = Path(f".env.{env}")

if not dotenv_path.exists():
    raise FileNotFoundError(f"ERROR '{env}' NOT FOUND: {dotenv_path}")

load_dotenv(dotenv_path)

class CURRENT_CONFIG:
    # generali
    SECRET_KEY = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # frontend
    FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")

    # database
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # SMTP
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
    SMTP_SSL = os.getenv("SMTP_SSL", "False").lower() == "true"

    # MinIO
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_SECURE = os.getenv("MINIO_SECURE", "False").lower() == "true"
    MINIO_BUCKET = os.getenv("MINIO_BUCKET")

    # Qdrant
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "files")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))

    # redis
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

    # Prompt
    REWRITER_SYSTEM_PROMPT = os.getenv("REWRITER_SYSTEM_PROMPT")
    RETRIEVAL_PROMPT_TEMPLATE = os.getenv("RETRIEVAL_PROMPT_TEMPLATE")
    GENERATOR_SYSTEM_PROMPT = os.getenv("GENERATOR_SYSTEM_PROMPT")