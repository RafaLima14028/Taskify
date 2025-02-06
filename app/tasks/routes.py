from fastapi import APIRouter

from app.tasks.db import DBTasks

router = APIRouter()

db = DBTasks()


@router.get("/tasks")
async def get_tasks() -> dict:
    try:
        return db.get_tasks()
    except Exception as e:
        return {"Error": str(e)}


@router.post("/tasks")
async def create_task(task: dict) -> dict:
    try:
        results = _check_task_is_valid(task)

        if isinstance(results, dict):
            return {"Error": str(e)}

        db.create_task(*results)

        return {"Message": f"Task created successfully!"}
    except Exception as e:
        return {"Error": str(e)}


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task: dict) -> dict:
    try:
        results = _check_task_is_valid(task)

        if isinstance(results, dict):
            return {"Error": str(e)}

        db.update_tasks(task_id, *results)

        return {"Message": f"Task {task_id} has been updated"}
    except Exception as e:
        return {"Error": str(e)}


def _check_task_is_valid(task: dict) -> dict | tuple:
    title = task.get("title", None)

    if not title:
        return {"Message": f"Error: The task has no title"}

    content = task.get("content", None)
    status = task.get("status", None)
    priority = task.get("priority", None)
    due_date = task.get("due_date", None)

    return title, content, status, priority, due_date
