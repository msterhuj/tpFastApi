from sqlalchemy import TEXT, Column
from sqlmodel import Field, SQLModel
from enum import Enum


class Severity(Enum):
    """
    Severity of the log message (info, warning, error)
    """
    INFO: str = "info"
    WARNING: str = "warning"
    ERROR: str = "error"


class Log(SQLModel, table=True):
    """
    Log model to store log messages
    """
    id: int = Field(default=None, primary_key=True)
    host: str = Field(nullable=False)
    service: str = Field(nullable=False)
    message: str = Field(sa_column=Column(TEXT))
    severity: Severity = Field(nullable=False)
    timestamp: int = Field(nullable=False)
