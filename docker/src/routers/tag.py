from fastapi import APIRouter, Depends

from src.schemas.tag import TagCreate, TagRead
from src.crud.tag import CRUDTag
from src.core.db_core import SessionDep
from src.routers.auth import get_current_user_dependency
from src.schemas.user import UserRead

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/")
async def get_all_tags(
    session: SessionDep,
    current_user: UserRead = Depends(get_current_user_dependency),
) -> list[TagRead]:
    return await CRUDTag().get_all_tags(session)


@router.post("/")
async def create_tag(
    tag: TagCreate,
    session: SessionDep,
    current_user: UserRead = Depends(get_current_user_dependency),
) -> TagRead:
    return await CRUDTag().create_tag(tag, session)
