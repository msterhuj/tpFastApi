from typing import Sequence

from fastapi import FastAPI
from sqlmodel import Session, select
from .models import User
from . import engine
from .database import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables(engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/")
def read_users() -> Sequence[User]:
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
