from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    ALLOWED_ORIGINS: str = "http://127.0.0.1:8080,http://localhost:8080"
    MAX_UPLOAD_SIZE: int = 52428800  # 50 MB en bytes
    RATE_LIMIT_PER_MINUTE: int = 3   # Máximo de peticiones por minuto por IP

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

settings = Settings()