from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "File Embedding Service"
    
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    
    CELERY_BROKER_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    CELERY_RESULT_BACKEND: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    ALLOWED_FILE_TYPES: List[str] = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    CHUNK_SIZE: int = 1000
    
    MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    class Config:
        case_sensitive = True

settings = Settings() 