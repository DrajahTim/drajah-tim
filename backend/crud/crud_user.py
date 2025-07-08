import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload # For eager loading if needed later

from backend.models.user import User
from backend.schemas.user import UserCreate
from backend.core.security import get_password_hash

async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
    """
    Retrieves a user by their ID.
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def get_user_by_phone(db: AsyncSession, phone_number: str) -> Optional[User]:
    """
    Retrieves a user by their phone number.
    """
    result = await db.execute(select(User).filter(User.phone_number == phone_number))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Retrieves a user by their email address.
    """
    if not email: # Guard against empty email string if it's optional but being queried
        return None
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        phone_number=user_in.phone_number,
        hashed_password=hashed_password,
        email=user_in.email,
        full_name=user_in.full_name,
        role=user_in.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Potential future CRUD operations for users:
# async def update_user(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
#     ...
# async def delete_user(db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
#     ...
