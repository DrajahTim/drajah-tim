from pydantic import BaseModel, EmailStr, constr
from typing import Optional
import uuid
from datetime import datetime

# Import the Enum from models to reuse it
from ..models.user import UserRole

class UserBase(BaseModel):
    phone_number: constr(min_length=10, max_length=15) # Basic validation
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: UserRole = UserRole.CUSTOMER

class UserCreate(UserBase):
    password: str # min_length can be added

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[constr(min_length=10, max_length=15)] = None
    # Password updates should be handled separately via a specific endpoint for security.
    # Role updates might also be restricted.

class User(UserBase): # Schema for reading user data, includes ID and timestamps
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # For Pydantic V2 compatibility with ORM models
