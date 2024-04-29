from enum import Enum
from typing import Optional

import hashlib
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str
    is_admin: bool = False


def get_hashed_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
