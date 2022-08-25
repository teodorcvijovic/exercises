from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class RecipeBase(BaseModel):
    class Config:
        orm_mode = True


class RecipeCreate(RecipeBase):
    name: str
    preparation: str
    ingredients: dict


class Recipe(RecipeBase):
    id: UUID
    name: str
    preparation: str
    ingredients: 'List[Ingredient]'
    created_at: datetime
    modified_at: Optional[datetime]


from .ingredient import Ingredient  # noqa

Recipe.update_forward_refs()
