from dotenv import load_dotenv
import os

load_dotenv()

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DEBUG = False
    SMTP_USER = os.environ.get("SMTP_USER")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
    SMTP_HOST = os.environ.get("SMTP_HOST")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 1025))
    FRONTEND_BASE_URL = os.environ.get("FRONTEND_BASE_URL")
    SMTP_SSL = os.environ.get("SMTP_SSL", "False").lower() == "true"
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_SECURE = os.getenv("MINIO_SECURE") == "true"
    MINIO_BUCKET = os.getenv("MINIO_BUCKET")
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "files")
    REWRITER_SYSTEM_PROMPT = os.getenv("REWRITER_SYSTEM_PROMPT")
    RETRIEVAL_PROMPT_TEMPLATE = os.getenv("RETRIEVAL_PROMPT_TEMPLATE")
    GENERATOR_SYSTEM_PROMPT = os.getenv("GENERATOR_SYSTEM_PROMPT")

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

env = os.getenv("FLASK_ENV", "development")
CONFIG_MAPPING = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

CURRENT_CONFIG = CONFIG_MAPPING.get(env, DevelopmentConfig)

class Config:
    pass  # Rimuovi le variabili prompt da qui
