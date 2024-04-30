from typing import Sequence

from fastapi import APIRouter
from sqlmodel import Session, select

from app.models import Log
from app import engine

router = APIRouter()


@router.get("/logs/", tags=["logs"])
def read_logs() -> Sequence[Log]:
    with Session(engine) as session:
        logs = session.exec(select(Log)).all()
        return logs
