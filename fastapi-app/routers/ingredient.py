from typing import Any


from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body

from dependencies import get_db
from services.ingredients import service_create_new_ingredient, \
    service_get_most_used_ingredients

from schemas.ingredient import Ingredient as IngredientSchema, \
    IngredientCreate

router = APIRouter(prefix='/ingredient')


# @router.post('/create', response_model=IngredientSchema)
# def create_new_ingredient(
#         ingredient: dict = Body(...), db: Session = Depends(get_db)
# ) -> Any:
#
#     new_ingredient = service_create_new_ingredient(ingredient, db)
#
#     return new_ingredient

@router.post('/create', response_model=IngredientSchema)
def create_new_ingredient(
        ingredient: IngredientCreate, db: Session = Depends(get_db)
) -> Any:

    new_ingredient = service_create_new_ingredient(ingredient, db)

    return new_ingredient


@router.get("/most_used")
def get_most_used_ingredients(number: int, db: Session = Depends(get_db)):

    ingredients = service_get_most_used_ingredients(number, db)

    return ingredients
