from fastapi import APIRouter
import jwt

from app.auth.utils import check_user_is_valid
from app.auth.db import DBAuth

router = APIRouter()

db = DBAuth()


@router.post("/auth")
async def login(user: dict) -> dict:
    results = check_user_is_valid(user)

    if isinstance(results, dict):
        return results

    try:
        user_exists = db.check_user(*results)

        return user_exists
    except Exception as e:
        return {"Error": str(e)}
