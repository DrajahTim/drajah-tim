from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

from . import Base # Changed from ..database import Base to . import Base

class Queue(Base):
    __tablename__ = "queues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False) # Can users join this queue?

    current_ticket_number_being_served = Column(Integer, default=0) # The ticket number currently being served
    last_issued_ticket_number = Column(Integer, default=0) # The last ticket number given out for this queue

    estimated_service_time_minutes = Column(Integer, nullable=True) # Average time in minutes per person/ticket
    service_specific_code = Column(String, nullable=True, unique=True, index=True) # Optional code for users to join

    max_concurrent_users = Column(Integer, nullable=True) # Max users allowed in queue at once
    operating_hours = Column(JSON, nullable=True) # E.g., {"Mon-Fri": "09:00-17:00", "Sat": "10:00-14:00"}

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    business = relationship("Business", back_populates="queues")
    entries = relationship("QueueEntry", back_populates="queue", cascade="all, delete-orphan", order_by="QueueEntry.ticket_number") # Order entries by ticket number

    def __repr__(self):
        return f"<Queue(id={self.id}, name='{self.name}', business_id='{self.business_id}')>"
