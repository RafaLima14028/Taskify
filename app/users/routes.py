from fastapi import APIRouter, Depends, HTTPException

from app.users.db import DBUsers
from app.utils import (
    check_user_is_valid,
    hashed_password,
    validate_token,
    UsernameOrEmailAlreadyBeenCreatedError,
)

router = APIRouter()

db = DBUsers()


@router.post("/users")
async def create_user(user: tuple = Depends(check_user_is_valid)) -> dict:
    try:
        username, email, password = user

        password = hashed_password(password)

        db.create_user(username, email, password)

        return {"Message": "User created successfully!"}
    except UsernameOrEmailAlreadyBeenCreatedError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/users")
async def update_user(
    user: tuple = Depends(check_user_is_valid), user_id: int = Depends(validate_token)
) -> dict:
    try:
        username, email, password = user

        password = hashed_password(password)

        db.update_user(user_id, username, email, password)

        return {"Message": "User updated successfully!"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@router.delete("/users")
async def delete_user(user_id: int = Depends(validate_token)) -> dict:
    try:
        db.delete_user(user_id)

        return {"Message": "User deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
