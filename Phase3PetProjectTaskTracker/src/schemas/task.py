from pydantic import BaseModel

from src.schemas.tag import TagRead


class TaskBase(BaseModel):
    title: str
    description: str
    deadline: str
    status: str


class TaskCreate(TaskBase):
    assignee_id: int | None = None

class TaskRead(TaskBase):
    id: int
    project_id: int
    assignee_id: int | None
    tags: list[TagRead] = []

class TaskUpdate(TaskBase):
    assignee_id: int | None = None

class TaskList(BaseModel):
    items: list[TaskRead]
    total: int