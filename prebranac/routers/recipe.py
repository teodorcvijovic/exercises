from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body

from dependencies import get_db
from models.ingredient import Ingredient
from models.recipe import Recipe

recipe_router = APIRouter()


@recipe_router.post('/v1', response_model=Any)
def create_new_recipe(
        recipe: dict = Body(...), db: Session = Depends(get_db)
) -> Any:
    """
    Create new recipe.
    :param recipe: Recipe model
    :param db: Current database session
    :returns: Newly created recipe
    """
    ingredient_list = []
    for ingredient_name in recipe['ingredients']:
        ingredient = db.query(Ingredient).filter(
            Ingredient.name == ingredient_name
        ).first()

        if ingredient:
            ingredient_list.append(ingredient)

    new_recipe = Recipe(
        name=recipe['name'],
        preparation=recipe['preparation'],
        ingredients=ingredient_list
    )

    db.add(new_recipe)
    db.commit()

    return recipe


@recipe_router.post('/v2')
def create_new_ingredient(
        ingredient: dict = Body(...), db: Session = Depends(get_db)
) -> Any:
    new_ingredient = Ingredient(name=ingredient['name'])

    db.add(new_ingredient)
    db.commit()

    return ingredient