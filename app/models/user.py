from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Roles(Enum):
    ADMIN: str = "admin"
    USER: str = "user"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str
    role: Roles
