from uuid import uuid4

from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    title: str
    done: bool = False


class Todo(TodoBase, table=True):
    id: str | None = Field(default_factory=lambda: str(uuid4()), primary_key=True)


class TodoCreate(TodoBase):
    ...
