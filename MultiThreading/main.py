import asyncio
import time

from fastapi import FastAPI
from starlette.background import BackgroundTasks

app = FastAPI()

def sync_task():
    time.sleep(3)
    print('Send email')

async def async_task():
    await asyncio.sleep(3)
    print('Send request to another API')

@app.post("/")
async def some_route(bg_tasks : BackgroundTasks):
    bg_tasks.add_task(sync_task)
#    asyncio.create_task(async_task())
    return {"ok" : True}