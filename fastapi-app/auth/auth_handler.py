import os
import time
from typing import Dict

import jwt

from models import User

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITM')


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user: User) -> Dict[str, str]:
    payload = {
        "username": user.username,
        "expires": time.time() + 600,  # 10 minutes

        # additional claims
        "firstname": user.firstname,
        "lastname": user.lastname
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token,
                                   JWT_SECRET,
                                   algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() \
            else None
    except:
        return {}
