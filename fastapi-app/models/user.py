import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime

from db.base_class import Base, UtcNow


class User(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True,
        nullable=False, default=uuid.uuid4
    )

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=UtcNow())


