from fastapi import APIRouter, Depends

from src.schemas.project import ProjectCreate
from src.schemas.user import UserRead
from src.crud.project import CRUDProject
from src.core.db_core import SessionDep
from src.routers.auth import get_current_user_dependency
from src.schemas.project import ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/")
async def create_project(project: ProjectCreate, session : SessionDep,  current_user: UserRead = Depends(get_current_user_dependency)):
    new_project = ProjectCreate(
        name=project.name,
    )
    return await CRUDProject().create_project(new_project, current_user.id, session)


@router.get("/all")
async def get_all_project(
    session: SessionDep,
    current_user: UserRead = Depends(get_current_user_dependency),
    limit: int = 20,
    offset: int = 0,
):
    return await CRUDProject().list_projects(current_user.id, session, limit, offset)

@router.get("/{id}")
async def get_project_by_id(id : int, session : SessionDep, current_user: UserRead = Depends(get_current_user_dependency)):
    return await CRUDProject().get_project(id, current_user.id, session)

@router.put("/{id}")
async def update_project(id : int, session : SessionDep, data : ProjectUpdate, current_user: UserRead = Depends(get_current_user_dependency)):
    return await CRUDProject().update_project(id, current_user.id, data, session)

@router.delete("/{id}")
async def delete_project(id : int, session : SessionDep, current_user: UserRead = Depends(get_current_user_dependency)):
    return await CRUDProject().delete_project(id, current_user.id, session)

