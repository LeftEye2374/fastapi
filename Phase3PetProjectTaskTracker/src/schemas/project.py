from pydantic import BaseModel

class ProjectBase(BaseModel):
    name : str


class ProjectCreate(ProjectBase):
    pass

class ProjectReade(ProjectBase):
    id : int
    owner_id : int

class ProjectUpdate(ProjectBase):
    pass