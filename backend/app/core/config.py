from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


def _split_csv(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    ENABLE_DOCS: bool = False
    
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    ALLOWED_ORIGINS: str = "http://localhost,https://localhost"
    CORS_ALLOW_CREDENTIALS: bool = False
    TRUSTED_HOSTS: str = "api.whatstats.net,www.whatstats.net,whatstats.net,localhost,127.0.0.1"
    MAX_UPLOAD_SIZE: int = 52428800  # 50 MB en bytes
    MAX_DECOMPRESSED_SIZE: int = 52428800  # 50 MB descomprimidos
    MAX_ZIP_COMPRESSION_RATIO: int = 100
    RATE_LIMIT_PER_MINUTE: int = 3   # Máximo de peticiones por minuto por IP

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> List[str]:
        return _split_csv(self.ALLOWED_ORIGINS)

    @property
    def trusted_hosts(self) -> List[str]:
        return _split_csv(self.TRUSTED_HOSTS)

settings = Settings()
