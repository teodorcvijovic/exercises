from sqlalchemy import func, desc

from models import Ingredient, recipe_ingredient


def service_create_new_ingredient(ingredient, db):
    new_ingredient = Ingredient(name=ingredient['name'])

    db.add(new_ingredient)
    db.commit()

    return ingredient


def service_get_most_used_ingredients(number, db):
    ingredients = db.query(Ingredient.name, func.count(recipe_ingredient.id)) \
        .join(
        recipe_ingredient,
        recipe_ingredient.ingredient == Ingredient.id
    ) \
        .group_by(Ingredient.name) \
        .order_by(desc(func.count(recipe_ingredient.id))) \
        .limit(number)

    return ingredients
