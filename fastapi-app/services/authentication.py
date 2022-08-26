from sqlalchemy.dialects.postgresql import psycopg2

from auth.auth_handler import signJWT
from exceptions import RecipeServerException
from models import User


def register(user, db):
    try:
        new_user = User(
            username=user.username,
            password=user.password,
            firstname=user.firstname,
            lastname=user.lastname
        )

        db.add(new_user)
        db.commit()

    except Exception:
        raise RecipeServerException(message='Error: User is already registered.',
                                    status_code=500)

    return signJWT(new_user)

def login(user, db):

    user_from_db = db.query(User).filter(User.username==user.username).first()

    if not user_from_db:
        raise RecipeServerException(message='Error: User does not exists.',
                                    status_code=500)

    if user_from_db.password != user.password:
        raise RecipeServerException(message='Error: Invalid password.',
                                    status_code=500)

    return signJWT(user_from_db)
