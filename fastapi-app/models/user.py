import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base, UtcNow


class User(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True,
        nullable=False, default=uuid.uuid4
    )

