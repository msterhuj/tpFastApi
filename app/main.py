from typing import Sequence
from pydantic import BaseModel

from fastapi import FastAPI
from sqlmodel import Session, select
from .models import User, Log, Severity
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


@app.get("/logs/")
def read_logs() -> Sequence[Log]:
    with Session(engine) as session:
        logs = session.exec(select(Log)).all()
        return logs


@app.get("/logs/{severity}")
def read_logs_by_severity(severity: Severity) -> Sequence[Log]:
    with Session(engine) as session:
        logs = session.exec(
            select(Log)
            .where(Log.severity == severity)
            .order_by(Log.id.desc())
        ).all()
        return logs


class LogInsert(BaseModel):
    host: str
    service: str
    message: str
    timestamp: int


@app.post("/logs/{severity}")
def create_log(severity: Severity, log: LogInsert):
    with Session(engine) as session:
        log = Log(
            host=log.host,
            service=log.service,
            message=log.message,
            severity=severity,
            timestamp=log.timestamp,
        )
        session.add(log)
        session.commit()
        session.refresh(log)
        return log
