from typing import Sequence, Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel
from sqlmodel import Session, select

from app.models import User, get_hashed_password
from app import engine, security
from app.models.user import is_admin

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    password: str
    password_confirm: str


@router.get("/users/", tags=["users"])
def read_users(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> Sequence[User]:
    if not is_admin(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


@router.post("/users/register", tags=["users"])
def create_user(user: UserCreate):
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    with Session(engine) as session:
        # Check if user already exists
        user_db = session.exec(select(User).where(User.name == user.name)).first()
        if user_db:
            raise HTTPException(status_code=400, detail="User already exists")
        # Create user
        user_db = User(name=user.name, password=get_hashed_password(user.password))
        session.add(user_db)
        session.commit()
        return {"id": user_db.id, "name": user_db.name}
