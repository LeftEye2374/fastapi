from fastapi import Depends
from fastapi import APIRouter
from src.schemas.user import UserCreate, UserRead
from src.crud.user import CRUDUser
from src.core.db_core import SessionDep
from src.core.security.security import security, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def create_user(user: UserCreate, session : SessionDep):
    new_user = UserCreate(
        email=user.email,
        name=user.name,
        password=user.password,
    )
    await CRUDUser().create_user(new_user, session)
    return {"User create is successful" : True}

@router.post("/login")
async def login_user(user: UserCreate, session: SessionDep = Depends(security)):
    current_user = await CRUDUser().get_user_by_email(user.email, session)
    if verify_password(user.password, current_user.password):
        security.create_access_token(data={"sub": user.email})

async def get_current_user_dependency(
    session: SessionDep,
    payload = Depends(security.access_token_required),
) -> UserRead:
    user_id = int(payload.sub)
    return await CRUDUser().get_user(user_id, session)

@router.get("/me")
async def get_current_user(current_user: UserRead = Depends(get_current_user_dependency)):
    return current_user