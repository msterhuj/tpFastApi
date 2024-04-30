from typing import Sequence, Type

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.models import Log, Severity
from app import engine

router = APIRouter()


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


@router.get("/logs/", tags=["logs"])
def read_logs() -> Sequence[Log]:
    with Session(engine) as session:
        logs = session.exec(select(Log)).all()
        return logs


@router.get("/logs/{severity}", tags=["logs"])
def read_logs_by_severity(severity: Severity) -> Sequence[Log]:
    with Session(engine) as session:
        logs = session.exec(
            select(Log)
            .where(Log.severity == severity)
            .order_by(Log.id.desc())
        ).all()
        return logs


@router.post("/logs/{severity}", tags=["logs"])
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


@router.patch("/logs/{log_id}", response_model=Log, tags=["logs"])
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


@router.delete("/logs/{log_id}", tags=["logs"])
def delete_log(log_id: int) -> dict[str, str]:
    with Session(engine) as session:
        db_log = session.get(Log, log_id)
        if db_log is None:
            raise HTTPException(status_code=404, detail="Log not found")
        session.delete(db_log)
        session.commit()
        return {"message": "Log deleted"}
