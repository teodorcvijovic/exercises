from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body

from dependencies import get_db
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
