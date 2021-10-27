import jwt
from jwt.exceptions import DecodeError

SECRET_KEY = "some_generated_secret_key"
ALGORITHM = "HS256"


def create_access_token(login_: str, pwd: str):
    return jwt.encode(
        {"login": login_, "password": pwd}, SECRET_KEY, algorithm=ALGORITHM
    )


def verify_token(encoded_jwt: str):
    try:
        return jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])
    except DecodeError:
        return None
