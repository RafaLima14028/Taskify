from fastapi import Header
import jwt
import bcrypt
from dotenv import load_dotenv
import os
from typing import Optional
from datetime import datetime

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTE"))


def check_username_and_password_is_valid(user: dict) -> dict | tuple:
    username = user.get("username", None)
    password = user.get("password", None)

    if (username is None) or (password is None):
        return {"Error": "username or password is null"}

    return username, password


def check_user_is_valid(user: dict) -> dict | tuple:
    username = user.get("username", None)
    email = user.get("email", None)
    password = user.get("password", None)

    if (username is None) or (email is None) or (password is None):
        return {"Error": "username, email or password is null"}

    return username, email, password


def check_task_is_valid(task: dict) -> dict | tuple:
    title = task.get("title", None)

    if not title:
        return {"Error": f"The task has no title"}

    content = task.get("content", None)
    status = task.get("status", None)
    priority = task.get("priority", None)
    due_date = task.get("due_date", None)

    return title, content, status, priority, due_date


def hashed_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    password_hash = bcrypt.hashpw(password_bytes, salt)

    return password_hash


def validate_token(authorization: Optional[str] = Header(None)) -> dict | int:
    if not authorization:
        return {"Error": "Token not provided"}

    try:
        token = authorization.split(" ")[1]

        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[
                ALGORITHM,
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
