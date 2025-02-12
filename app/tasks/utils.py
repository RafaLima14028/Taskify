from fastapi import Header
import jwt
from typing import Optional, Annotated
from datetime import datetime

__SECRET_KEY = "KEY"
__ALGORITHM = "HS256"
__ACCESS_TOKEN_EXPIRE_MINUTES = 30


def check_task_is_valid(task: dict) -> dict | tuple:
    title = task.get("title", None)

    if not title:
        return {"Error": f"The task has no title"}

    content = task.get("content", None)
    status = task.get("status", None)
    priority = task.get("priority", None)
    due_date = task.get("due_date", None)

    return title, content, status, priority, due_date


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
