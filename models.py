from uuid import uuid4

from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    name: str
    title: bool = Field(default=False)


class Todo(TodoBase, table=True):
    id: str | None = Field(default_factory=lambda: str(uuid4()), primary_key=True)


class TodoCreate(TodoBase):
    ...
