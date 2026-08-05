from fastapi import HTTPException

from src.schemas.user import UserUpdate, UserCreate
from src.core.db_core import SessionDep
from src.core.security.security import hash_password
from src.schemas.user import UserRead
from src.models.Models import Users

class CRUDUser:

    async def create_user(self, data: UserCreate, session: SessionDep) -> UserRead:
        user = Users(
            name=data.name,
            email=data.email,
            hashed_password=await hash_password(data.password),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return UserRead.model_validate(user, from_attributes=True)


    async def get_user(self, id: int, session: SessionDep) -> UserRead:
        user = await session.get(Users, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.model_validate(user, from_attributes=True)

    async def get_user_by_email(self, email: str, session: SessionDep) -> UserCreate:
        user = await session.get(Users, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserCreate.model_validate(user, from_attributes=True)


    async def update_user(self, id: int, data: UserUpdate, session: SessionDep) -> UserRead:
        user = await session.get(Users, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.name = data.name
        user.email = data.email
        await session.commit()
        return UserRead.model_validate(user, from_attributes=True)

    async def delete_user(self, id: int, session: SessionDep):
        user = await session.get(Users, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        await session.commit()
