from fastapi import APIRouter
import jwt
from datetime import datetime, timedelta

from app.utils import (
    check_username_and_password_is_valid,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
)
from app.auth.db import DBAuth

router = APIRouter()

db = DBAuth()


@router.post("/auth")
async def login(user: dict) -> dict:
    results = check_username_and_password_is_valid(user)

    if isinstance(results, dict):
        return results

    try:
        user_exists = db.check_user(*results)
        exists_id = user_exists.get("ID", None)

        if exists_id is not None:
            token_data = {
                "sub": str(exists_id),
                "exp": datetime.utcnow()
                + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

            return {"Access Token": token, "Token Type": "bearer"}

        return user_exists
    except Exception as e:
        return {"Error": str(e)}
