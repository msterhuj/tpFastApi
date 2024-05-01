from fastapi import FastAPI

from . import engine, views
from .database import create_db_and_tables

app = FastAPI()

app.include_router(views.log_router)
app.include_router(views.user_router)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables(engine)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}
