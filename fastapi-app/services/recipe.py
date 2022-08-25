from sqlalchemy import func

from models import Ingredient, Recipe, recipe_ingredient


def service_create_new_recipe(recipe, db):
    ingredients = {}
    for ingredient_name in recipe['ingredients'].keys():
        ingredient = db.query(Ingredient) \
            .filter(Ingredient.name == ingredient_name) \
            .first()

        if not ingredient:
            return {'message': f'Error: Ingredient {ingredient_name} does '
                               f'not exists.'}

        ingredients[ingredient] = recipe['ingredients'][ingredient_name]

    try:
        new_recipe = Recipe(
            name=recipe['name'],
            preparation=recipe['preparation'],
            # ingredients=[ingredient for ingredient in ingredients.keys()]
        )

        db.add(new_recipe)
        db.commit()

        for ingredient in ingredients.keys():
            new_recipe_ingredient = recipe_ingredient(
                recipe=new_recipe.id,
                ingredient=ingredient.id,
                quantity=ingredients[ingredient]
            )
            db.add(new_recipe_ingredient)

        db.commit()

        return {'message': f'Recipe {new_recipe.name} successfully created.'}

    except KeyError:
        return {'message': 'Error: Arguments missing'}


def service_get_recipe_by_name(recipe_name, db):
    recipe = db.query(Recipe).filter(Recipe.name == recipe_name).first()

    if not recipe:
        return {'message': 'Error: Recipe does not exists.'}
    else:
        return str(recipe)


def service_get_recipes_with_max_ingredients(db):
    def max_ingredients():
        ingredients_count = db.query(Recipe.name,
                                     func.count(recipe_ingredient.id)
                                     .label('count')
                                     ) \
            .join(
            recipe_ingredient,
            recipe_ingredient.recipe == Recipe.id
        ) \
            .group_by(Recipe.name) \
            .subquery()

        max_ingredient_number = db.query(
            func.max(ingredients_count.c.count)
        ) \
            .scalar()

        return max_ingredient_number

    recipes = db.query(Recipe.name, func.count(recipe_ingredient.id)) \
        .join(
        recipe_ingredient,
        recipe_ingredient.recipe == Recipe.id
    ) \
        .group_by(Recipe.name) \
        .having(
        func.count(recipe_ingredient.id) == max_ingredients()
    )

    return recipes
