from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings

from routers.recipe import router as recipe_router
from routers.ingredient import router as ingredient_router

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
