from fastapi import APIRouter
import jwt
from datetime import datetime, timedelta

from app.auth.utils import check_user_is_valid
from app.auth.db import DBAuth

router = APIRouter()

db = DBAuth()


__SECRET_KEY = "KEY"
__ALGORITHM = "HS256"
__ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/auth")
async def login(user: dict) -> dict:
    results = check_user_is_valid(user)

    if isinstance(results, dict):
        return results

    try:
        user_exists = db.check_user(*results)
        exists_id = user_exists.get("ID", None)

        if exists_id is not None:
            token_data = {
                "sub": str(exists_id),
                "exp": datetime.utcnow()
                + timedelta(minutes=__ACCESS_TOKEN_EXPIRE_MINUTES),
            }
            token = jwt.encode(token_data, __SECRET_KEY, algorithm=__ALGORITHM)

            return {"Access Token": token, "Token Type": "bearer"}

        return user_exists
    except Exception as e:
        return {"Error": str(e)}
