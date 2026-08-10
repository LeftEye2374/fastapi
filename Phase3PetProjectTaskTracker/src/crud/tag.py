from fastapi import HTTPException

from src.schemas.tag import TagCreate, TagRead
from src.models.Models import Tags, Tasks
from src.core.db_core import SessionDep
from sqlalchemy import select


class CRUDTag():

    async def create_tag(self, data: TagCreate, session) -> TagRead:
        new_tag = Tags(
            name=data.name,
        )
        session.add(new_tag)
        await session.commit()
        await session.refresh(new_tag)
        return TagRead.model_validate(new_tag, from_attributes=True)


    async def get_all_tags(self, session: SessionDep) -> list[TagRead]:
        result = await session.execute(select(Tags))
        tags = result.scalars().all()
        return [TagRead.model_validate(t, from_attributes=True) for t in tags]

    async def add_tag_to_task(self, task_id: int, tag_id: int, current_user_id: int, session: SessionDep):
        task = await session.get(Tasks, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await session.refresh(task, attribute_names=["project", "tags"])
        if task.project.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not your task")

        tag = await session.get(Tags, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        if tag not in task.tags:
            task.tags.append(tag)
            await session.commit()

    async def remove_tag_from_task(self, task_id: int, tag_id: int, current_user_id: int, session: SessionDep):
        task = await session.get(Tasks, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await session.refresh(task, attribute_names=["project", "tags"])
        if task.project.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not your task")

        tag = await session.get(Tags, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        if tag in task.tags:
            task.tags.remove(tag)
            await session.commit()