from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteException

from config import settings
from exceptions import generic_error_handler, recipe_server_exception_handler, \
    RecipeServerException
from logger import LOG_CONFIG

from routers.recipe import router as recipe_router
from routers.ingredient import router as ingredient_router
from routers.authentication import router as authentication_router

# Setup logging configuration
dictConfig(LOG_CONFIG)

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_STR}/openapi.json'
)

# Middleware setup
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

# Attach API routers
app.include_router(recipe_router, prefix=settings.API_STR)
app.include_router(ingredient_router, prefix=settings.API_STR)
app.include_router(authentication_router, prefix=settings.API_STR)

# Add error handlers
app.add_exception_handler(Exception, generic_error_handler)
app.add_exception_handler(
    RecipeServerException, recipe_server_exception_handler
)
# app.add_exception_handler(StarletteException, recipe_server_exception_handler)
