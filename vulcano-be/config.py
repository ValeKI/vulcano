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
