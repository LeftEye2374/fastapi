from sqlalchemy.testing.pickleable import User

from fastapi import Depends
from main import app
from schemas.user import UserCreate
from src.crud.user import CRUDUser
from src.core.security.security import security


@app.post("/auth/register")
async def create_user(user: UserCreate):
    password = security.hash_password(user.password)
    new_user = UserCreate(
        email=user.email,
        name=user.name,
        password=password,
    )
    CRUDUser.create_user(new_user)
    return {"User create is successful", True}

@app.post("/auth/login")
async def login_user(user: UserCreate):
    ...

@app.get("/auth/me")
async def get_current_user(current_user: User = Depends(get_current_user)):
    ...