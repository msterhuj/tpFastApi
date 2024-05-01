from datetime import datetime, UTC
from typing import Sequence

from fastapi import APIRouter, HTTPException, Depends
from jose import jwt
from pydantic import BaseModel
from sqlmodel import Session, select

from app.models import User, get_hashed_password, verify_password
from app import engine, tokens_forgery
from app.models.user import TokenTable

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    password: str
    password_confirm: str


class RequestDetails(BaseModel):
    name: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ChangePassword(BaseModel):
    name: str
    old_password: str
    new_password: str
    new_password_confirm: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime


@tokens_forgery.token_required
@router.get("/users/", tags=["users"])
def read_users(dependencies=Depends(tokens_forgery.JWTBearer())) -> Sequence[User]:
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


@router.post("/users/login", tags=["users"], response_model=TokenSchema)
def login(request: RequestDetails):
    with Session(engine) as session:
        user_db = session.exec(select(User).where(User.name == request.name)).first()
        if not user_db or not verify_password(request.password, user_db.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        access_token = tokens_forgery.create_access_token(user_db.id)
        refresh_token = tokens_forgery.create_refresh_token(user_db.id)

        token_db: TokenTable = TokenTable(
            user_id=user_db.id,
            access_token=access_token,
            refresh_token=refresh_token,
            status=True,
            created_date=datetime.now()
        )
        session.add(token_db)
        session.commit()
        session.refresh(token_db)
        return {"access_token": access_token, "refresh_token": refresh_token}


@router.post('/logout')
def logout(dependencies=Depends(tokens_forgery.JWTBearer())):
    with Session(engine) as db:
        token = dependencies
        payload = jwt.decode(token, tokens_forgery.JWT_SECRET_KEY, tokens_forgery.ALGORITHM)
        user_id = payload['sub']
        token_record = db.query(TokenTable).all()
        info = []
        for record in token_record:
            print("record", record)
            if (datetime.now(UTC) - record.created_date).days > 1:
                info.append(record.user_id)
        if info:
            existing_token = db.query(TokenTable).where(TokenTable.user_id.in_(info)).delete()
            db.commit()

        existing_token = db.query(TokenTable).filter(TokenTable.user_id == user_id,
                                                     TokenTable.access_token == token).first()
        if existing_token:
            existing_token.status = False
            db.add(existing_token)
            db.commit()
            db.refresh(existing_token)
        return {"message": "Logout Successfully"}
