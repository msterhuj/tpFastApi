import os
from datetime import datetime, timedelta, UTC
from functools import wraps
from typing import Union, Any

from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from .models import get_hashed_password, verify_password
from .models.user import TokenTable

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "abcdefghjiqlmnopqrstuvwxyz"
JWT_REFRESH_SECRET_KEY = "0123456789"


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        data = kwargs['session'].query(TokenTable).filter_by(
            user_id=user_id,
            access_toke=kwargs['dependencies'],
            status=True).first()
        if data:
            return func(kwargs['dependencies'], kwargs['session'])

        else:
            return {'msg': "Token blocked"}

    return wrapper


def decode_token(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
        return decoded_token
    except jwt.JWTError:
        return None


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(UTC) + expires_delta

    else:
        expires_delta = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(UTC) + expires_delta
    else:
        expires_delta = datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_token(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


jwt_bearer = JWTBearer()
