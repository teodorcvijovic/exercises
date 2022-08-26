import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base, UtcNow

from .recipe_ingredient import RecipeIngredient


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
        'Ingredient', secondary=RecipeIngredient.__table__,
        back_populates='recipes', cascade='all, delete'
    )

    def __repr__(self):
        ingredient_names = [ingredient.name for ingredient in self.ingredients]
        recipe_string = f'{self.name}['
        for i in range(len(ingredient_names)):
            recipe_string += f'{ingredient_names[i]}'
            if i < len(ingredient_names) - 1:
                recipe_string += ', '
        recipe_string += '] (preparation: ' + self.preparation + ')'
        return recipe_string
