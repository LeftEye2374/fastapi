from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskList
from src.core.db_core import SessionDep
from src.models.Models import Tasks, Projects


class CRUDTask:

    async def create_task(self, data : TaskCreate, project_id : int, assignee_id: int, session : SessionDep) -> TaskRead:
        task = Tasks(
            project_id = project_id,
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            status=data.status,
            assignee_id=assignee_id,
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        await session.refresh(task, attribute_names=["tags"])
        return TaskRead.model_validate(task, from_attributes=True)

    async def update_task(self, task_id : int, data : TaskUpdate, assignee_id: int | None, current_user_id : int, session : SessionDep ) -> TaskRead:
        task = await session.get(Tasks, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await session.refresh(task, attribute_names=["project"])
        if task.project.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not your task")
        task.title = data.title
        task.description = data.description
        task.deadline = data.deadline
        task.status = data.status
        task.assignee_id = assignee_id
        await session.commit()
        await session.refresh(task, attribute_names=["tags"])
        return TaskRead.model_validate(task, from_attributes=True)

    async def delete_task(self, task_id: int, current_user_id: int, session: SessionDep):
        task = await session.get(Tasks, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await session.refresh(task, attribute_names=["project"])
        if task.project.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not your task")
        await session.delete(task)
        await session.commit()

    async def get_all_tasks_of_project(
        self,
        project_id: int,
        current_user_id: int,
        session: SessionDep,
        limit: int = 20,
        offset: int = 0,
        status: str | None = None,
        assignee_id: int | None = None,
    ) -> TaskList:
        project = await session.get(Projects, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not your project")

        conditions = [Tasks.project_id == project_id]
        if status is not None:
            conditions.append(Tasks.status == status)
        if assignee_id is not None:
            conditions.append(Tasks.assignee_id == assignee_id)

        total = (
            await session.execute(
                select(func.count()).select_from(Tasks).where(*conditions)
            )
        ).scalar_one()

        result = await session.execute(
            select(Tasks)
            .where(*conditions)
            .options(selectinload(Tasks.tags))
            .limit(limit)
            .offset(offset)
        )
        tasks = result.scalars().all()
        return TaskList(
            items=[TaskRead.model_validate(t, from_attributes=True) for t in tasks],
            total=total,
        )

    async def get_task_by_id(self,task_id : int, current_user_id: int, session : SessionDep) -> TaskRead:
        task = await session.get(Tasks, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await session.refresh(task, attribute_names=["project", "tags"])
        if task.project.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not your task")
        return TaskRead.model_validate(task, from_attributes=True)
