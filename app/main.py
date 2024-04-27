from typing import Sequence, Type
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from .models import User, Log, Severity
from . import engine
from .database import create_db_and_tables

app = FastAPI()


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


class LogUpdate(BaseModel):
    host: str | None = None
    service: str | None = None
    message: str | None = None
    timestamp: int | None = None


@app.post("/logs/{severity}")
def create_log(severity: Severity, log: LogInsert) -> Log:
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


@app.patch("/logs/{log_id}", response_model=Log)
def update_log(log_id: int, log: LogUpdate) -> Type[Log] | None:
    with Session(engine) as session:
        db_log = session.get(Log, log_id)
        if db_log is None:
            raise HTTPException(status_code=404, detail="Log not found")
        log_data = log.model_dump(exclude_unset=True)
        db_log.sqlmodel_update(log_data)
        session.add(db_log)
        session.commit()
        session.refresh(db_log)
        return db_log


@app.delete("/logs/{log_id}")
def delete_log(log_id: int) -> dict[str, str]:
    with Session(engine) as session:
        db_log = session.get(Log, log_id)
        if db_log is None:
            raise HTTPException(status_code=404, detail="Log not found")
        session.delete(db_log)
        session.commit()
        return {"message": "Log deleted"}
