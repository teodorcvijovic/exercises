import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base, UtcNow


class Recipe(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True,
        nullable=False, default=uuid.uuid4
    )
    name = Column(String, unique=True, nullable=False, index=True)
    preparation = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=UtcNow())
    modified_at = Column(DateTime(timezone=True), onupdate=UtcNow())
    ingredients = relationship(
        'Ingredient', secondary='recipe_ingredient',
        back_populates='recipes', cascade='all, delete'
    )

