from pydantic import BaseModel
from typing import Optional
import uuid

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[uuid.UUID] = None
    # You can add other fields like roles, permissions if needed in the token
    # phone_number: Optional[str] = None # Example if you want phone_number in token payload
