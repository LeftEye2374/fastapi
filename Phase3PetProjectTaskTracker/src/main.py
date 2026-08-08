from fastapi import FastAPI
from src.routers.auth import router as auth_router
from src.routers.project import router as project_router
from src.routers.task import router as task_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)