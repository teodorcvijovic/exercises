import logging

from sqlalchemy import func, desc

from models import Ingredient, RecipeIngredient

logger = logging.getLogger(__name__)

def service_create_new_ingredient(ingredient, db):
    new_ingredient = Ingredient(name=ingredient.name)

    db.add(new_ingredient)
    db.commit()

    logger.info(f'Successfully added new ingredient: {new_ingredient.name}')

    return new_ingredient


def service_get_most_used_ingredients(number, db):
    ingredients = db.query(Ingredient.name, func.count(
                        RecipeIngredient.id.label('count'))
                    ) \
                    .join(
                        RecipeIngredient,
                        RecipeIngredient.ingredient == Ingredient.id
                    ) \
                    .group_by(Ingredient.name) \
                    .order_by(desc(func.count(RecipeIngredient.id))) \
                    .limit(number)

    return ingredients
