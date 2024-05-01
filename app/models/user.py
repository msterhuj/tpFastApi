from typing import Optional

import hashlib

from fastapi.security import HTTPBasicCredentials
from sqlalchemy import Column, TEXT
from sqlmodel import Field, SQLModel, Session, select
from datetime import datetime

from app import engine


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    password: str
    is_admin: bool = False


def is_valid_user(credentials: HTTPBasicCredentials) -> bool:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.name == credentials.username)).first()
        if not user:
            return False
        return verify_password(credentials.password, user.password)


def is_admin(credentials: HTTPBasicCredentials) -> bool:
    if not is_valid_user(credentials):
        return False
    with Session(engine) as session:
        user = session.exec(select(User).where(User.name == credentials.username)).first()
        if not user:
            return False
        return user.is_admin


def get_hashed_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_hashed_password(plain_password) == hashed_password
