from uuid import uuid4

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str


class User(UserBase, table=True):
    id: str | None = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    hashed_password: str


class UserCreateSerializer(UserBase):
    password: str = Field(..., min_length=8)


class UserResponseSerializer(UserBase):
    id: str
