import uvicorn
from fastapi import FastAPI
app = FastAPI()

@app.get("/", summary="Main root", tags=["root"])
async def home():
    return "Hello World"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
