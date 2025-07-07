import enum
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

from . import Base # Changed from ..database import Base to . import Base

class QueueEntryStatus(str, enum.Enum):
    WAITING = "waiting"         # User is in queue, waiting
    CALLED = "called"           # User has been notified, turn is approaching
    NEXT = "next"               # User is the next to be served
    SERVING = "serving"         # User is currently being served
    SERVED = "served"           # User's service is complete
    CANCELLED_USER = "cancelled_by_user"     # User cancelled their spot
    CANCELLED_SYSTEM = "cancelled_by_system" # System cancelled (e.g., business closed)
    NO_SHOW = "no_show"         # User was called but did not show up

class QueueEntry(Base):
    __tablename__ = "queue_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    queue_id = Column(UUID(as_uuid=True), ForeignKey("queues.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    ticket_number = Column(Integer, nullable=False) # Assigned when joining; needs logic for generation (e.g., sequential per queue)

    status = Column(SAEnum(QueueEntryStatus), nullable=False, default=QueueEntryStatus.WAITING, index=True)

    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    called_at = Column(DateTime(timezone=True), nullable=True) # Timestamp when user is notified (e.g., 5 places away)
    service_start_time = Column(DateTime(timezone=True), nullable=True) # Timestamp when actual service begins
    served_at = Column(DateTime(timezone=True), nullable=True) # Timestamp when service ends / entry is completed

    estimated_wait_time_at_join_minutes = Column(Integer, nullable=True) # Snapshot of EWT when user joined

    priority_level = Column(Integer, default=0, nullable=False) # 0 for normal, higher for priority

    notes_by_user = Column(Text, nullable=True)
    notes_by_staff = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) # Redundant with joined_at but good for audit
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    # Relationships
    queue = relationship("Queue", back_populates="entries")
    user = relationship("User", back_populates="queue_entries")

    def __repr__(self):
        return f"<QueueEntry(id={self.id}, queue_id='{self.queue_id}', user_id='{self.user_id}', ticket_number={self.ticket_number}, status='{self.status}')>"
