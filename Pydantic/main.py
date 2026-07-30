from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, ConfigDict

app = FastAPI()

data = {
    "email": "abc@mail.com",
    "bio": "hello, its",
    "age": 12,
}

class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=10)

    model_config = ConfigDict(extra = "forbid")

class UserWithAgeSchema(UserSchema):
    age: int = Field(ge=0, le = 130)

users = []

@app.get("/users")
def get_all_users():
    return users

@app.post("/users")
def add_user(user : UserSchema):
    users.append(user)
    return {"ok": True, "msg": "User added"}


def func(data_ : dict):
    data_["age"] += 1