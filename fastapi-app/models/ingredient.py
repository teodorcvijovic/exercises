import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base, UtcNow

from .recipe_ingredient import RecipeIngredient


class Ingredient(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True,
        nullable=False, default=uuid.uuid4
    )

    name = Column(String, unique=True, nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=UtcNow())
    modified_at = Column(DateTime(timezone=True), onupdate=UtcNow())

    recipes = relationship(
        'Recipe', secondary=RecipeIngredient.__table__,
        back_populates='ingredients', cascade='all, delete'
    )
