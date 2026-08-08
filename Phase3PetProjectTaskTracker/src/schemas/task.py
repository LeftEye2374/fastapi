from pydantic import BaseModel


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

class TaskUpdate(TaskBase):
    assignee_id: int | None = None