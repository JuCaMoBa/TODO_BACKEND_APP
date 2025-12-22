"""Funciones utilitarias para la autenticacion con JWT."""

from typing import Optional
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from core.settings.settings import settings

from api.v1.schemas.auth.auth_token import UserAuthData


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un token de acceso JWT."""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        secret_key = settings.SECRETE_KEY
        algorithm = settings.ALGORITHM
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating access token: {e}")
    return encoded_jwt


def verify_access_token(token: str):
    """Verifica y decodifica un token de acceso JWT."""
    try:
        payload = jwt.decode(token, settings.SECRETE_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        email = payload.get("email")
        user_id = payload.get("user_id")
        is_active = payload.get("is_active")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return UserAuthData(
        username=username,
        email=email,
        user_id=user_id,
        is_active=is_active
    )
