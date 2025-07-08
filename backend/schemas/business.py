from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
import uuid
from datetime import datetime
from .user import User # To show owner details

class BusinessBase(BaseModel):
    name: str
    category: str
    address: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[constr(min_length=5, max_length=20)] = None # Basic validation
    is_active: bool = True

class BusinessCreate(BusinessBase):
    # owner_id will be set from the authenticated user context, not directly from payload
    pass

class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[constr(min_length=5, max_length=20)] = None
    is_active: Optional[bool] = None

class Business(BusinessBase): # Schema for reading business data
    id: uuid.UUID
    owner_id: uuid.UUID
    # owner: Optional[User] = None # Optionally include full owner details
    created_at: datetime
    updated_at: datetime

    # queues: List['Queue'] = [] # Forward reference for Queue schema, handled later

    class Config:
        from_attributes = True

# Forward reference for Queue needs to be resolved after Queue schema is defined.
# This is typically done by calling model_rebuild() on the models in Pydantic v2.
from .queue import Queue # Import Queue here
Business.model_rebuild() # Pydantic v2
