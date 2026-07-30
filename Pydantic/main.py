from pydantic import BaseModel, Field, EmailStr, ConfigDict

data = {
    "email": "abc@mail.com",
    "bio": "hello, its",
    "age": 12,
    "gender": "male",
    "birthday": "2022",
}

class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=10)

    model_config = ConfigDict(extra = "forbid")

class UserWithAgeSchema(UserSchema):
    age: int = Field(ge=0, le = 130)


user = UserSchema(**data)
user_with_age = UserWithAgeSchema(**data)
print(repr(user))
print(repr(user_with_age))


def func(data_ : dict):
    data_["age"] += 1