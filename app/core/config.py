from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Image Processor API"
    PROJECT_VERSION: str = "1.0.0"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    FIREBASE_STORAGE_BUCKET: str
    FIREBASE_DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
