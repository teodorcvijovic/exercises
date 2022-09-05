from typing import Any


from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends


from dependencies import get_db

from services.recipe import service_create_new_recipe, \
    service_get_recipe_by_name, service_get_recipes_with_max_ingredients

from schemas.recipe import Recipe as RecipeSchema, RecipeCreate

router = APIRouter(prefix='/recipe')


@router.post('/create', response_model=RecipeSchema)
def create_new_recipe(
        recipe: RecipeCreate, db: Session = Depends(get_db)
) -> Any:
    # recipe - contains name, preparation and dict[ingredient]=quantity

    response = service_create_new_recipe(recipe, db)

    return response


@router.get("/get")
def get_recipe_by_name(recipe_name: str, db: Session = Depends(get_db)):

    recipes = service_get_recipe_by_name(recipe_name, db)

    return recipes


@router.get("/max_ingredients")
def get_recipes_with_max_ingredients(db: Session = Depends(get_db)):

    recipes = service_get_recipes_with_max_ingredients(db)

    return recipes
