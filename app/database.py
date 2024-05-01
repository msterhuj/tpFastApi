from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel
from os import environ


def init_engine() -> Engine:
    """
    Initialize the database engine
    :return: Engine object
    """
    return create_engine(environ.get("DB_URI"), echo=True)


def create_db_and_tables(engine: Engine) -> None:
    """
    Create the database and tables
    :param engine: Engine object
    :return: None
    """
    SQLModel.metadata.create_all(engine)
