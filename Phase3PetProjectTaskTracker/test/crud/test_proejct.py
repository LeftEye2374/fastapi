import pytest
from fastapi import HTTPException

from src.crud.project import CRUDProject
from src.schemas.project import ProjectCreate


@pytest.mark.asyncio
async def test_create_project_sets_owner(db_session):
    project = await CRUDProject().create_project(
        ProjectCreate(name="Solo"), owner_id=1, session=db_session
    )
    assert project.owner_id == 1
    assert project.id is not None


@pytest.mark.asyncio
async def test_get_project_wrong_owner_raises_403(db_session):
    created = await CRUDProject().create_project(
        ProjectCreate(name="Solo"), owner_id=1, session=db_session
    )
    with pytest.raises(HTTPException) as exc_info:
        await CRUDProject().get_project(created.id, current_user_id=2, session=db_session)
    assert exc_info.value.status_code == 403
