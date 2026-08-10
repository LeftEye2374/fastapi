from fastapi import APIRouter, Depends

from src.crud.task import CRUDTask
from src.crud.tag import CRUDTag
from src.core.db_core import SessionDep
from src.routers.auth import get_current_user_dependency
from src.schemas.user import UserRead

from src.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/")
async def create_task(task : TaskCreate, project_id : int, session : SessionDep, current_user: UserRead = Depends(get_current_user_dependency)):
    assignee_id = task.assignee_id if task.assignee_id is not None else current_user.id
    return await CRUDTask().create_task(task, project_id, assignee_id, session)

@router.get("/all")
async def get_all_tasks(
    project_id: int,
    session: SessionDep,
    current_user: UserRead = Depends(get_current_user_dependency),
    limit: int = 20,
    offset: int = 0,
    status: str | None = None,
    assignee_id: int | None = None,
):
    return await CRUDTask().get_all_tasks_of_project(
        project_id, current_user.id, session, limit, offset, status, assignee_id
    )

@router.get("/{id}")
async def get_task_by_id(id : int, session : SessionDep, current_user: UserRead = Depends(get_current_user_dependency)):
    return await CRUDTask().get_task_by_id(id, current_user.id, session)

@router.put("/{id}")
async def update_task(id : int, data : TaskUpdate, session : SessionDep, current_user: UserRead = Depends(get_current_user_dependency)):
    return await CRUDTask().update_task(id, data, data.assignee_id, current_user.id, session)

@router.delete("/{id}")
async def delete_task(id : int, session : SessionDep, current_user: UserRead = Depends(get_current_user_dependency)):
    return await CRUDTask().delete_task(id, current_user.id, session)

@router.post("/{id}/tags/{tag_id}")
async def add_tag_to_task(id : int, tag_id : int, session : SessionDep, current_user: UserRead = Depends(get_current_user_dependency)):
    await CRUDTag().add_tag_to_task(id, tag_id, current_user.id, session)
    return {"success": True}

@router.delete("/{id}/tags/{tag_id}")
async def remove_tag_from_task(id : int, tag_id : int, session : SessionDep, current_user: UserRead = Depends(get_current_user_dependency)):
    await CRUDTag().remove_tag_from_task(id, tag_id, current_user.id, session)
    return {"success": True}
