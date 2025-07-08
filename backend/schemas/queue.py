from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
# from .business import Business # To show business details if needed
# from .queue_entry import QueueEntry # To show entries if needed

class QueueBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    estimated_service_time_minutes: Optional[int] = None
    service_specific_code: Optional[str] = None
    max_concurrent_users: Optional[int] = None
    operating_hours: Optional[Dict[str, str]] = None # e.g. {"Mon-Fri": "09:00-17:00"}

    @validator('estimated_service_time_minutes', 'max_concurrent_users')
    def check_positive(cls, value):
        if value is not None and value < 0:
            raise ValueError('must be a positive integer or null')
        return value

class QueueCreate(QueueBase):
    # business_id will be set from context or path parameter usually
    pass

class QueueUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    estimated_service_time_minutes: Optional[int] = None
    service_specific_code: Optional[str] = None # Consider uniqueness constraint handling
    max_concurrent_users: Optional[int] = None
    operating_hours: Optional[Dict[str, str]] = None
    current_ticket_number_being_served: Optional[int] = None # Allow admin to adjust
    last_issued_ticket_number: Optional[int] = None # Allow admin to adjust (carefully)


class Queue(QueueBase): # Schema for reading Queue data
    id: uuid.UUID
    business_id: uuid.UUID
    current_ticket_number_being_served: int
    last_issued_ticket_number: int
    created_at: datetime
    updated_at: datetime

    # business: Optional[Business] = None # To show full business details
    # entries: List[QueueEntry] = [] # To show current entries in the queue

    class Config:
        from_attributes = True

# Forward reference resolution for Business and QueueEntry
from .business import BusinessBase # Using Base to avoid circular full model
from .queue_entry import QueueEntry # Using full model if it doesn't cause deep recursion for typical use cases
Queue.model_rebuild()
Business.model_rebuild() # Ensure Business is also rebuilt if it references Queue
QueueEntry.model_rebuild() # Ensure QueueEntry is rebuilt
