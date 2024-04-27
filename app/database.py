from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}


def init_engine() -> Engine:
    return create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables(engine: Engine):
    SQLModel.metadata.create_all(engine)
