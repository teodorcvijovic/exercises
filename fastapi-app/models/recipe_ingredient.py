import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey

from db.base_class import Base, UtcNow


class recipe_ingredient(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True,
        nullable=False, default=uuid.uuid4
    )

    recipe = Column(UUID(as_uuid=True), ForeignKey("recipe.id"))
    ingredient = Column(UUID(as_uuid=True), ForeignKey("ingredient.id"))
    quantity = Column(String, nullable=True, default="1")

    created_at = Column(DateTime(timezone=True), server_default=UtcNow())
    modified_at = Column(DateTime(timezone=True), onupdate=UtcNow())
