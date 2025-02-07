from fastapi import FastAPI
import uvicorn

from app.tasks.routes import router as tasks_router

app = FastAPI()

app.include_router(tasks_router, prefix="/api", tags=["tasks"])


@app.get("/")
async def home():
    return {"Message": "Hello to Taskify"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=34827, reload=True)
