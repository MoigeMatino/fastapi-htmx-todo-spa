from uuid import uuid4

from sqlmodel import Field, Relationship, SQLModel


class TodoBase(SQLModel):
    title: str
    done: bool = False


class Todo(TodoBase, table=True):
    id: str | None = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str | None = Field(default=None, foreign_key="user.id")

    user: "User" = Relationship(back_populates="todos")  # type: ignore # noqa: F821
    file_path: str | None = None
    file_name: str | None = None


class TodoCreate(TodoBase):
    file: str | None = None
