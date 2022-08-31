import os
from pathlib import Path
from typing import List, Union

from dotenv import load_dotenv  # pip install python-dotenv
from pydantic import AnyHttpUrl, BaseSettings

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    API_STR: str = '/api'

    # defined in .env

    PROJECT_NAME: str = os.getenv('PROJECT_NAME')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    HOST: Union[str, None] = os.getenv('HOST') or '0.0.0.0'
    PORT: Union[int, None] = os.getenv('PORT') or 8080
    CORS_ORIGINS: List[AnyHttpUrl] = [
        os.getenv('LOCAL_ORIGIN')
    ]

    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER', 'localhost')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')

    DB_URL: str = os.getenv('DB_URL')

    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID') or None
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET') or None

    # end

    # SQLALCHEMY_DATABASE_URL = (
    #     f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    #     f'@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
    # )
    SQLALCHEMY_DATABASE_URL = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{DB_URL}/{POSTGRES_DB}'
    )


class Config:
    case_sensitive = True


settings = Settings()
