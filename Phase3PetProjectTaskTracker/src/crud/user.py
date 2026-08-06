
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from src.schemas.user import UserUpdate, UserCreate
from src.core.db_core import SessionDep
from src.core.security.security import hash_password
from src.schemas.user import UserRead
from src.models.Models import Users
from sqlalchemy import select

class CRUDUser:

    async def create_user(self, data: UserCreate, session: SessionDep) -> UserRead:
        user = Users(
            name=data.name,
            email=data.email,
            hashed_password=await hash_password(data.password),
        )
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=409, detail="Email already registered")
        await session.refresh(user)
        return UserRead.model_validate(user, from_attributes=True)


    async def get_user(self, id: int, session: SessionDep) -> UserRead:
        user = await session.get(Users, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.model_validate(user, from_attributes=True)

    async def get_user_by_email(self, email: str, session: SessionDep) -> Users | None:
        result = await session.execute(select(Users).where(Users.email == email))
        return result.scalar_one_or_none()


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
