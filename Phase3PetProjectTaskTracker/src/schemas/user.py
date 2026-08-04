from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password : str

class UserRead(UserBase):
    id : int

class UserUpdate(UserBase):
    pass
