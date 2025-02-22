from fastapi import APIRouter, Depends, HTTPException

from app.tasks.db import DBTasks
from app.utils import validate_token, check_task_is_valid

router = APIRouter()

db = DBTasks()


@router.get("/tasks")
async def get_tasks(user_id: int = Depends(validate_token)) -> dict:
    try:
        return db.get_tasks(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks")
async def create_task(
    task: tuple = Depends(check_task_is_valid), user_id: int = Depends(validate_token)
) -> dict:
    try:
        db.create_task(user_id, *task)

        return {"Message": f"Task created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task: tuple = Depends(check_task_is_valid),
    user_id: int = Depends(validate_token),
) -> dict:
    try:
        db.update_tasks(user_id, task_id, *task)

        return {"Message": f"Task {task_id} has been updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
