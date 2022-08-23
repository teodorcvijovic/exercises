from typing import List, Union
from pydantic import AnyHttpUrl, BaseSettings
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    API_STR: str = '/api'
    PROJECT_NAME: str = os.getenv('PROJECT_NAME')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    HOST: Union[str, None] = os.getenv('HOST') or '0.0.0.0'
    PORT: Union[int, None] = os.getenv('PORT') or 8080
    CORS_ORIGINS: List[AnyHttpUrl] = [
        os.getenv('LOCAL_ORIGINS')
    ]

    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER') or 'localhost'
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT') or '5432'
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URL = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )

    class Config:
        case_sensitive = True


settings = Settings()
