from sqlmodel import Field, SQLModel
from enum import Enum


class Severity(Enum):
    INFO: str = "info"
    WARNING: str = "warning"
    ERROR: str = "error"


class Log(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    host: str = Field(nullable=False)
    service: str = Field(nullable=False)
    message: str = Field(nullable=False)
    severity: Severity = Field(nullable=False)
    timestamp: int = Field(nullable=False)