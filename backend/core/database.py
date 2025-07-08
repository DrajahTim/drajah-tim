from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from backend.core.config import settings
# Assuming your models' Base is defined in backend/models/__init__.py
# from backend.models import Base # Not strictly needed here for session, but good for create_all if used

# Create an asynchronous engine
# The 'future=True' flag is default in SQLAlchemy 2.0 for engines and enables 2.0 style usage.
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for debugging SQL statements
    future=True
)

# Create an asynchronous session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Good practice for FastAPI to prevent issues with background tasks
    autocommit=False,
    autoflush=False,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async database session.
    Ensures the session is closed after the request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # If you want to commit automatically after each successful request processing:
            # await session.commit()
            # However, it's often better to commit explicitly in the CRUD operations or service layer.
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Optional: Function to create all tables (useful for initial setup or testing, not for production with Alembic)
# async def create_db_and_tables():
#     async with async_engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all) # To drop all tables
#         await conn.run_sync(Base.metadata.create_all)
#
# Example usage (e.g., in main.py for initial setup if not using Alembic):
# import asyncio
# from backend.models import Base # Make sure all your models are imported in models/__init__
#
# async def init_db():
#     async with async_engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all) # Use with caution
#         await conn.run_sync(Base.metadata.create_all)
#
# if __name__ == "__main__":
# asyncio.run(init_db())
