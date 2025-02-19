from fastapi import APIRouter, Depends, HTTPException
import jwt
from datetime import datetime, timedelta

from app.utils import (
    IncorrectPasswordError,
    NotFoundUserError,
    check_username_and_password_is_valid,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
)
from app.auth.db import DBAuth

router = APIRouter()

db = DBAuth()


@router.post("/auth")
async def login(user: tuple = Depends(check_username_and_password_is_valid)) -> dict:
    try:
        id_user = db.check_user(*user)

        token_data = {
            "sub": str(id_user),
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return {"Access Token": token, "Token Type": "bearer"}
    except IncorrectPasswordError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except NotFoundUserError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
