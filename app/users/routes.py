from fastapi import APIRouter

from app.users.db import DBUsers
from app.users.utils import check_user_is_valid, hashed_password

router = APIRouter()

db = DBUsers()


@router.post("/users")
async def create_user(user: dict) -> dict:
    try:
        results = check_user_is_valid(user)

        if isinstance(results, dict):
            return results

        username, email, password = results

        password = hashed_password(password)

        db.create_user(username, email, password)

        return {"Message": "User created successfully!"}
    except Exception as e:
        return {"Error": str(e)}


@router.put("/users/{user_id}")
async def update_user(user_id: int, user: dict) -> dict:
    try:
        results = check_user_is_valid(user)

        if isinstance(results, dict):
            return results

        username, email, password = results

        password = hashed_password(password)

        db.update_user(user_id, username, email, password)

        return {"Message": "User updated successfully!"}
    except Exception as e:
        return {"Error": str(e)}


@router.delete("/users/{user_id}")
async def delete_user(user_id: int) -> dict:
    try:
        db.delete_user(user_id)

        return {"Message": "User deleted successfully!"}
    except Exception as e:
        return {"Error": str(e)}
