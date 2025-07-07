# This directory can hold core configuration files and utilities.
# For example:
# - config.py (for environment variables and settings)
# - database.py (for database session management if using SQLAlchemy)
# - security.py (for password hashing, JWT token creation/verification)

# Example: backend/core/config.py
#
# from pydantic_settings import BaseSettings
#
# class Settings(BaseSettings):
#     API_V1_STR: str = "/api/v1"
#     DATABASE_URL: str = "postgresql://user:password@host:port/dbname"
#     SECRET_KEY: str = "a_very_secret_key"  # Used for JWT
#     ALGORITHM: str = "HS256" # Algorithm for JWT
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#
#     class Config:
#         env_file = ".env" # If you use a .env file for environment variables
#
# settings = Settings()

# Example: backend/core/database.py (for SQLAlchemy)
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from .config import settings
#
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
#
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
