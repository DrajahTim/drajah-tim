# This directory will contain Pydantic schemas for data validation and serialization.
# These schemas define the expected structure of API request and response bodies.

# For example: backend/schemas/queue.py
#
# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime
#
# class QueueBase(BaseModel):
#     name: str
#     description: Optional[str] = None
#     location: Optional[str] = None
#
# class QueueCreate(QueueBase):
#     pass
#
# class Queue(QueueBase):
#     id: int
#     manager_id: int
#     created_at: datetime
#     current_token_number: Optional[int] = None
#     estimated_wait_time_minutes: Optional[int] = None
#
#     class Config:
#         orm_mode = True # For SQLAlchemy compatibility
#
#
# Example: backend/schemas/user.py
#
# from pydantic import BaseModel, EmailStr
#
# class UserBase(BaseModel):
#     email: EmailStr
#
# class UserCreate(UserBase):
#     password: str
#
# class User(UserBase):
#     id: int
#     is_active: bool
#
#     class Config:
#         orm_mode = True
