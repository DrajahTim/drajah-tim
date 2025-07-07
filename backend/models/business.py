from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

from . import Base # Changed from ..database import Base to . import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True) # E.g., "Hospital", "Bank", "Restaurant", "Salon"
    address = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False) # Link to the User who owns/manages this business

    is_active = Column(Boolean, default=True, nullable=False) # Business can be deactivated

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="businesses_managed", foreign_keys=[owner_id])
    queues = relationship("Queue", back_populates="business", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Business(id={self.id}, name='{self.name}', owner_id='{self.owner_id}')>"
