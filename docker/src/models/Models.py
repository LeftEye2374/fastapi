from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db_core import Base


class Users(Base):

    __tablename__ = 'user'

    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(unique=True)
    name : Mapped[str]
    hashed_password : Mapped[str]

    projects : Mapped[list["Projects"]] = relationship(
        back_populates="owner",
    )

    assigned_tasks: Mapped[list["Tasks"]] = relationship(
        back_populates="assignee"
    )

class Projects(Base):

    __tablename__ = 'project'

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]

    owner: Mapped["Users"] = relationship(
        back_populates="projects"
    )

    owner_id : Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )

    tasks : Mapped[list["Tasks"]] = relationship(
        back_populates="project",
        cascade="all, delete, delete-orphan",
    )

class Tasks(Base):

    __tablename__ = 'task'

    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    deadline: Mapped[str]
    status: Mapped[str]
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id")
    )
    assignee_id : Mapped[int | None] = mapped_column(
        ForeignKey("user.id")
    )

    project: Mapped["Projects"] = relationship(
        back_populates="tasks"
    )

    assignee: Mapped["Users | None"] = relationship(
        back_populates="assigned_tasks"
    )

    tags: Mapped[list["Tags"]] = relationship(
        secondary="task_tag",
        back_populates="tasks"
    )

class Tags(Base):

    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    tasks: Mapped[list["Tasks"]] = relationship(
        secondary="task_tag",
        back_populates="tags"
    )

class TaskTags(Base):

    __tablename__ = 'task_tag'

    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id"),
        primary_key=True
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id"),
        primary_key=True
    )