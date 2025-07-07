from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "QueueMe API"
    API_V1_STR: str = "/api/v1"

    # Database settings
    # Example: "postgresql+asyncpg://user:password@localhost:5432/queueme_db"
    # It's recommended to set this in your .env file
    DATABASE_URL: str = "postgresql+asyncpg://your_db_user:your_db_password@localhost:5432/queueme_app_db"

    # JWT settings - IMPORTANT: Change SECRET_KEY in your .env file for production!
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # Default, override in .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # 30 minutes
    # REFRESH_TOKEN_EXPIRE_DAYS: int = 7 # Example for refresh tokens, if implemented

    # Optional: Email settings for notifications (if we add them later)
    # MAIL_USERNAME: Optional[str] = None
    # MAIL_PASSWORD: Optional[str] = None
    # MAIL_FROM: Optional[str] = None
    # MAIL_PORT: Optional[int] = None
    # MAIL_SERVER: Optional[str] = None
    # MAIL_STARTTLS: bool = True
    # MAIL_SSL_TLS: bool = False

    # Configure Pydantic to load from a .env file and ignore extra fields
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


settings = Settings()

# To use these settings in other modules:
# from backend.core.config import settings
# print(settings.DATABASE_URL)
