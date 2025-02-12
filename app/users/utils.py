from fastapi import Header
import jwt
from typing import Optional
from datetime import datetime
import bcrypt

__SECRET_KEY = "KEY"
__ALGORITHM = "HS256"
__ACCESS_TOKEN_EXPIRE_MINUTES = 30


def check_user_is_valid(user: dict) -> dict | tuple:
    username = user.get("username", None)
    email = user.get("email", None)
    password = user.get("password", None)

    if (username is None) or (email is None) or (password is None):
        return {"Error": "username, email or password is null"}

    return username, email, password


def hashed_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    password_hash = bcrypt.hashpw(password_bytes, salt)

    return password_hash


def check_hashed_password(password: str, hashed_password: bytes) -> bool:
    password_bytes = password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password)


def validate_token(authorization: Optional[str] = Header(None)) -> dict | int:
    if not authorization:
        return {"Error": "Token not provided"}

    try:
        token = authorization.split(" ")[1]

        payload = jwt.decode(
            jwt=token,
            key=__SECRET_KEY,
            algorithms=[
                __ALGORITHM,
            ],
        )

        if payload.get("exp") > datetime.utcnow().timestamp():
            return {"Error": "Token expired"}

        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return {"Error": "Token expired"}
    except jwt.InvalidTokenError as e:
        print(e)
        return {"Error": "Token invalid"}
