from fastapi import APIRouter, Depends

from app.users.db import DBUsers
from app.utils import check_user_is_valid, hashed_password, validate_token

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


@router.put("/users")
async def update_user(user: dict, user_id=Depends(validate_token)) -> dict:
    if isinstance(user_id, dict):
        return user_id

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


@router.delete("/users")
async def delete_user(user_id=Depends(validate_token)) -> dict:
    if isinstance(user_id, dict):
        return user_id

    try:
        db.delete_user(user_id)

        return {"Message": "User deleted successfully!"}
    except Exception as e:
        return {"Error": str(e)}
