from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, ForeignKey, Column

from db.base_class import Base

recipe_ingredient = Table(
    'recipe_ingredient',
    Base.metadata,
    Column(
        'recipe_id', UUID(as_uuid=True),
        ForeignKey('recipe.id'), primary_key=True
    ),
    Column(
        'ingredient_id', UUID(as_uuid=True),
        ForeignKey('ingredient.id'), primary_key=True
    )
)