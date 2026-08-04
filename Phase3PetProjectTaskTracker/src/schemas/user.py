from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    email : EmailStr
    password : str
    name : str

class UserRead(BaseModel):
    id : int
    email : str
    name : str
