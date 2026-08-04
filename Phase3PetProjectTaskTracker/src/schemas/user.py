from pydantic import BaseModel
from pydantic.v1 import EmailStr


class UserCreate(BaseModel):
    email : EmailStr
    password : str
    name : str

class UserRead(BaseModel):
    id : int
    email : str
    name : str
