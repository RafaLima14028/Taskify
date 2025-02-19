from fastapi import Header, HTTPException
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


class IncorrectPasswordError(Exception):
    def __init__(self):
        super().__init__("Incorrect password")


class NotFoundUserError(Exception):
    def __init__(self):
        super().__init__("User not exists in database")


class UsernameOrEmailAlreadyBeenCreatedError(Exception):
    def __init__(self):
        super().__init__("This user or email has already been created")


def check_username_and_password_is_valid(user: dict) -> tuple:
    username = user.get("username", None)
    password = user.get("password", None)

    if (username is None) or (password is None):
        raise HTTPException(status_code=400, detail="username or password is null")

    return username, password


def check_user_is_valid(user: dict) -> tuple:
    username = user.get("username", None)
    email = user.get("email", None)
    password = user.get("password", None)

    if (username is None) or (email is None) or (password is None):
        raise HTTPException(
            status_code=400, detail="username, email or password is null"
        )

    return username, email, password


def check_task_is_valid(task: dict) -> tuple:
    title = task.get("title", None)

    if not title:
        raise HTTPException(status_code=400, detail="The task has no title")

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


def validate_token(authorization: Optional[str] = Header(None)) -> int:
    if not authorization:
        raise HTTPException(status_code=400, detail="Token not provided")

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
            raise HTTPException(status_code=401, detail="Token expired")

        return int(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Token invalid")
