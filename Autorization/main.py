from fastapi import FastAPI
from authx import AuthX, AuthXConfig
app = FastAPI()

@app.post("/login")
def login():
    ...

@app.get("/protected")
def protected():
    ...