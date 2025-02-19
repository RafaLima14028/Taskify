from fastapi import FastAPI
import uvicorn
import ssl

from app.users.routes import router as users_router
from app.tasks.routes import router as tasks_router
from app.auth.routes import router as auth_router

app = FastAPI()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("certificates/cert.pem", keyfile="certificates/key.pem")

app.include_router(users_router, prefix="/api", tags=["users"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(auth_router, prefix="/api", tags=["auth"])


@app.get("/")
async def home():
    return {"Message": "Hello to Taskify"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=34827,
        reload=True,
        workers=4,
        ssl_keyfile="certificates/key.pem",
        ssl_certfile="certificates/cert.pem",
    )
