from authlib.integrations.base_client import OAuthError
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from auth.auth_handler import decodeJWT
from dependencies import get_db
from schemas.user import RegistrationScheme, LoginScheme

from services.authentication import register as service_register
from services.authentication import login as service_login


router = APIRouter()


@router.post('/register')
def register(user: RegistrationScheme, db: Session = Depends(get_db)):
    jwt_token = service_register(user, db)

    return jwt_token


@router.post('/mylogin')
def register(user: LoginScheme, db: Session = Depends(get_db)):
    jwt_token = service_login(user, db)

    return jwt_token



