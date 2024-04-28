from enum import Enum
from typing import Optional

from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Roles(Enum):
    ADMIN: str = "admin"
    USER: str = "user"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str
    role: Roles


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)
