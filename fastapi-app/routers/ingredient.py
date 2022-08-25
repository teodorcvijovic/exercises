from typing import Any

from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body

from dependencies import get_db
from models import recipe_ingredient
from models.ingredient import Ingredient
from models.recipe import Recipe

router = APIRouter(prefix='/ingredient')


@router.post('/create')
def create_new_ingredient(
        ingredient: dict = Body(...), db: Session = Depends(get_db)
) -> Any:
    new_ingredient = Ingredient(name=ingredient['name'])

    db.add(new_ingredient)
    db.commit()

    return ingredient


@router.get("/most_used")
def get_most_used_ingredients(number: int, db: Session = Depends(get_db)):

    ingredients = db.query(Ingredient.name, func.count(recipe_ingredient.id)) \
               .join(
                        recipe_ingredient,
                        recipe_ingredient.ingredient == Ingredient.id
                     ) \
               .group_by(Ingredient.name) \
               .order_by(desc(func.count(recipe_ingredient.id))) \
               .limit(number)

    return ingredients
