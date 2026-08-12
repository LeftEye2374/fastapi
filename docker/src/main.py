import logging
import time

from fastapi import FastAPI, Request

from src.routers.auth import router as auth_router
from src.routers.project import router as project_router
from src.routers.task import router as task_router
from src.routers.tag import router as tag_router

logger = logging.getLogger("task_tracker")
logger.setLevel(logging.INFO)
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
    logger.addHandler(_handler)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s -> %s (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(tag_router)
