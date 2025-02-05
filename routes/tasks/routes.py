from fastapi import APIRouter

router = APIRouter()

tasks = []


@router.get("/tasks")
async def get_tasks():
    return {"Tasks": tasks}


@router.post("/tasks")
async def create_task(task: dict):
    tasks.append(task)

    return {"Message": f"Task '{task}' created successfully!"}
