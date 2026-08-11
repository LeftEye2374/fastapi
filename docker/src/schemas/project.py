from pydantic import BaseModel

class ProjectBase(BaseModel):
    name : str


class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id : int
    owner_id : int

class ProjectUpdate(ProjectBase):
    pass

class ProjectList(BaseModel):
    items: list[ProjectRead]
    total: int

