from typing import Optional

import hashlib

from sqlalchemy import Column, TEXT
from sqlmodel import Field, SQLModel
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    password: str
    is_admin: bool = False


class TokenTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    access_token: str = Field(sa_column=Column(TEXT))
    refresh_token: str = Field(sa_column=Column(TEXT))
    status: bool = Field(default=True)
    created_at: datetime = Field(default=datetime.now())


def get_hashed_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_hashed_password(plain_password) == hashed_password
