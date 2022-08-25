# Import all the models, so that Base has them before being
# imported by Alembic
from db.base_class import Base # noqa
from models.ingredient import Ingredient # noqa
from models.recipe import Recipe # noqa
from models.recipe_ingredient import recipe_ingredient # noqa
