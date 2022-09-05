from pydantic import BaseModel


class UserScheme(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class LoginScheme(UserScheme):
    pass


class RegistrationScheme(UserScheme):
    firstname: str
    lastname: str
