from typing import Sequence, Type, Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel
from sqlmodel import Session, select

from app.models import Log, Severity
from app import engine, security
from app.models.user import is_admin, is_valid_user

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
def read_logs(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> Sequence[Log]:
    if not is_valid_user(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    with Session(engine) as session:
        logs = session.exec(select(Log)).all()
        return logs


@router.get("/logs/{severity}", tags=["logs"])
def read_logs_by_severity(severity: Severity, credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> Sequence[Log]:
    if not is_valid_user(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    with Session(engine) as session:
        logs = session.exec(
            select(Log)
            .where(Log.severity == severity)
            .order_by(Log.id.desc())
        ).all()
        return logs


@router.post("/logs/{severity}", tags=["logs"])
def create_log(severity: Severity, log: LogInsert, credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> Log:
    if not is_valid_user(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
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
def update_log(log_id: int, log: LogUpdate, credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> Type[Log] | None:
    if not is_admin(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
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
def delete_log(log_id: int, credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> dict[str, str]:
    if not is_admin(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    with Session(engine) as session:
        db_log = session.get(Log, log_id)
        if db_log is None:
            raise HTTPException(status_code=404, detail="Log not found")
        session.delete(db_log)
        session.commit()
        return {"message": "Log deleted"}
