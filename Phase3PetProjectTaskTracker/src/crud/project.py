from fastapi import HTTPException

from src.schemas.project import ProjectRead, ProjectUpdate, ProjectCreate
from src.core.db_core import SessionDep
from src.models.Models import Projects
from sqlalchemy import select


class CRUDProject:

    async def create_project(self, data: ProjectCreate, owner_id: int, session: SessionDep) -> ProjectRead:
        project = Projects(
            name=data.name,
            owner_id=owner_id,
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return ProjectRead.model_validate(project, from_attributes=True)

    async def update_project(self, project_id : int, current_user_id: int, data : ProjectUpdate, session : SessionDep) -> ProjectRead:
        project = await session.get(Projects, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if current_user_id != project.owner_id:
            raise HTTPException(status_code=403, detail="You can't update your own project")
        project.name = data.name
        await session.commit()
        return ProjectRead.model_validate(project, from_attributes=True)

    async def delete_project(self, project_id: int, current_user_id: int, session: SessionDep):
        project = await session.get(Projects, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if current_user_id != project.owner_id:
            raise HTTPException(status_code=403, detail="You can't update your own project")
        await session.delete(project)
        await session.commit()


    async def get_project(self, project_id : int, current_user_id: int, session : SessionDep) -> ProjectRead:
        project = await session.get(Projects, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if current_user_id != project.owner_id:
            raise HTTPException(status_code=403, detail="You can't update your own project")
        return ProjectRead.model_validate(project, from_attributes=True)

    async def list_projects(self, owner_id: int, session: SessionDep) -> list[ProjectRead]:
        result = await session.execute(select(Projects).where(Projects.owner_id == owner_id))
        projects = result.scalars().all()
        return [ProjectRead.model_validate(p, from_attributes=True) for p in projects]