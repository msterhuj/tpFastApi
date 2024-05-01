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
    """
    UserCreate is a Pydantic model that represents the data required to create a new user.
    """
    name: str
    password: str
    password_confirm: str


class UserShow(BaseModel):
    """
    UserList is a Pydantic model that represents a list of users.
    """
    name: str
    is_admin: bool
    id: int


@router.get("/users/", tags=["users"])
def read_users(credentials: Annotated[HTTPBasicCredentials, Depends(security)], response_model=list[UserShow]) -> Sequence[UserShow]:
    """
    read_users is a FastAPI route that returns all users. Requires authentication.
    :param credentials: The credentials of the user.
    :return: A list of all users.
    """
    if not is_admin(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


@router.post("/users/register", tags=["users"])
def create_user(user: UserCreate):
    """
    create_user is a FastAPI route that creates a new user.
    :param user: The data required to create a new user.
    :return: The created user information.
    """
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
