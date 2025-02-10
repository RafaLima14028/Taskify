from fastapi import APIRouter

from app.tasks.db import DBTasks
from app.tasks.utils import check_task_is_valid

router = APIRouter()

db = DBTasks()


@router.get("/tasks/{user_id}")
async def get_tasks(user_id: int) -> dict:
    try:
        return db.get_tasks(user_id)
    except Exception as e:
        return {"Error": str(e)}


@router.post("/tasks/{user_id}")
async def create_task(user_id: int, task: dict) -> dict:
    try:
        results = check_task_is_valid(task)

        if isinstance(results, dict):
            return {"Error": str(e)}

        db.create_task(user_id, *results)

        return {"Message": f"Task created successfully!"}
    except Exception as e:
        return {"Error": str(e)}


@router.put("/tasks/{user_id}/{task_id}")
async def update_task(user_id: int, task_id: int, task: dict) -> dict:
    try:
        results = check_task_is_valid(task)

        if isinstance(results, dict):
            return results

        db.update_tasks(user_id, task_id, *results)

        return {"Message": f"Task {task_id} has been updated"}
    except Exception as e:
        return {"Error": str(e)}
