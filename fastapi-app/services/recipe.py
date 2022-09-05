from sqlalchemy import func

from exceptions import RecipeServerException
from models import Ingredient, Recipe, RecipeIngredient


def service_create_new_recipe(recipe, db):
    ingredients = {}
    for ingredient_name in recipe.ingredients.keys():
        ingredient = db.query(Ingredient) \
            .filter(Ingredient.name == ingredient_name) \
            .first()

        if not ingredient:
            raise RecipeServerException(
                status_code=404,
                message='Error: Ingredient does not exists.'
            )

        ingredients[ingredient] = recipe.ingredients[ingredient_name]

    try:
        new_recipe = Recipe(
            name=recipe.name,
            preparation=recipe.preparation,
            # ingredients=[ingredient for ingredient in ingredients.keys()]
        )

        db.add(new_recipe)
        db.commit()

        for ingredient in ingredients.keys():
            new_recipe_ingredient = RecipeIngredient(
                recipe=new_recipe.id,
                ingredient=ingredient.id,
                quantity=ingredients[ingredient]
            )
            db.add(new_recipe_ingredient)

        db.commit()

        return new_recipe

    except KeyError:
        raise RecipeServerException(
            status_code=404,
            message='Error: Arguments missing.'
        )


def service_get_recipe_by_name(recipe_name, db):
    recipe = db.query(Recipe).filter(Recipe.name == recipe_name).first()

    if not recipe:
        raise RecipeServerException(
            status_code=404,
            message='Error: Recipe does not exist.'
        )
    else:
        return str(recipe)


def service_get_recipes_with_max_ingredients(db):
    def max_ingredients():
        ingredients_count = db.query(Recipe.name,
                                     func.count(RecipeIngredient.id)
                                     .label('count')
                                     ) \
            .join(
                RecipeIngredient,
            RecipeIngredient.recipe == Recipe.id
            ) \
            .group_by(Recipe.name) \
            .subquery()

        max_ingredient_number = db.query(
                func.max(ingredients_count.c.count)
            ) \
            .scalar()

        return max_ingredient_number

    recipes = db.query(Recipe.name, func.count(RecipeIngredient.id)) \
        .join(
            RecipeIngredient,
        RecipeIngredient.recipe == Recipe.id
        ) \
        .group_by(Recipe.name) \
        .having(
        func.count(RecipeIngredient.id) == max_ingredients()
        )

    return recipes
