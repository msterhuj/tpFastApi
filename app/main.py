from typing import Sequence, Type
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from .models import User, Log, Severity, get_hashed_password
from . import engine, views
from .database import create_db_and_tables

app = FastAPI()

app.include_router(views.log_router)

@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables(engine)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/users/")
def read_users() -> Sequence[User]:
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


class UserInsert(BaseModel):
    name: str
    password: str
    password_confirm: str


@app.post("/users/register")
def create_user(user: UserInsert):
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    with Session(engine) as session:
        # Check if user already exists
        user_db = session.exec(select(User).where(User.name == user.name)).first()
        if user_db:
            raise HTTPException(status_code=400, detail="User already exists")
        # Create user
        user_db = User(name=user.name, password=get_hashed_password(user.password))
        session.add(user_db)
        session.commit()
        return {"id": user_db.id, "name": user_db.name}
