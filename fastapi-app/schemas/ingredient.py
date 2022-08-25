from uuid import UUID
from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: UUID
