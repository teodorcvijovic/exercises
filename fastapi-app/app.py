from logging.config import dictConfig

from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, Request
from starlette.config import Config
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteException
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse

from config import settings
from exceptions import generic_error_handler, recipe_server_exception_handler, \
    RecipeServerException
from logger import LOG_CONFIG

from routers.recipe import router as recipe_router
from routers.ingredient import router as ingredient_router
from routers.authentication import router as authentication_router

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Setup logging configuration
dictConfig(LOG_CONFIG)

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_STR}/openapi.json'
)

# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': settings.GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
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

if settings.SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# app.add_middleware(HTTPSRedirectMiddleware)

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

# oauth endpoints

@app.get('/')
def public(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
    return HTMLResponse('<a href=/login>Login</a>')


@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for(
        'auth')  # This creates the url for our /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    user_data = await oauth.google.parse_id_token(request, access_token)
    request.session['user'] = dict(user_data)
    return RedirectResponse(url='/')
