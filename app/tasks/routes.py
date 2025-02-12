from fastapi import APIRouter, Depends

from app.tasks.db import DBTasks
from app.tasks.utils import check_task_is_valid, validate_token

router = APIRouter()

db = DBTasks()


@router.get("/tasks/")
async def get_tasks(user_id=Depends(validate_token)) -> dict:
    if isinstance(user_id, dict):
        return user_id

    try:
        return db.get_tasks(user_id)
    except Exception as e:
        return {"Error": str(e)}


@router.post("/tasks/")
async def create_task(task: dict, user_id=Depends(validate_token)) -> dict:
    if isinstance(user_id, dict):
        return user_id

    try:
        results = check_task_is_valid(task)

        if isinstance(results, dict):
            return {"Error": str(e)}

        db.create_task(user_id, *results)

        return {"Message": f"Task created successfully!"}
    except Exception as e:
        return {"Error": str(e)}


@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int, task: dict, user_id=Depends(validate_token)
) -> dict:
    try:
        results = check_task_is_valid(task)

        if isinstance(results, dict):
            return results

        db.update_tasks(user_id, task_id, *results)

        return {"Message": f"Task {task_id} has been updated"}
    except Exception as e:
        return {"Error": str(e)}
