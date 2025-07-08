import enum
from sqlalchemy import Column, Integer, String, DateTime, func, Enum as SAEnum
from sqlalchemy.orm import relationship
import uuid # For UUID primary keys
from sqlalchemy.dialects.postgresql import UUID # Import UUID type for PostgreSQL

from . import Base # Changed from ..database import Base to . import Base

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    BUSINESS_ADMIN = "business_admin"
    STAFF = "staff"
    SUPER_ADMIN = "super_admin" # For app-level administration

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True, index=True)
    password_hash = Column(String, nullable=False) # Store hashed passwords, not plain text

    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.CUSTOMER)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    businesses_managed = relationship("Business", back_populates="owner", foreign_keys="[Business.owner_id]")
    queue_entries = relationship("QueueEntry", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, phone_number='{self.phone_number}', role='{self.role}')>"
