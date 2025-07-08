from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import models here to ensure they are registered with Base
from .user import User, UserRole
from .business import Business
from .queue import Queue
from .queue_entry import QueueEntry, QueueEntryStatus

# This allows Alembic to find the models if you're using it for migrations.
# And makes them easily importable from `models` package, e.g. `from models import User`
__all__ = [
    "Base",
    "User",
    "UserRole",
    "Business",
    "Queue",
    "QueueEntry",
    "QueueEntryStatus",
]
