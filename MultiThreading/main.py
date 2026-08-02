import asyncio
import time

from fastapi import FastAPI

app = FastAPI()

def sync_task():
    time.sleep(3)
    print('Send email')

async def async_task():
    await asyncio.sleep(3)
    print('Send request to another API')