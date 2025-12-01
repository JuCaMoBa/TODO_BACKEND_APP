"""Funciones utilitarias para la autenticacion con JWT."""

import os
from typing import Optional
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un token de acceso JWT."""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        secret_key = os.getenv("SECRETE_KEY")
        algorithm = os.getenv("ALGORITHM")
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating access token: {e}")
    return encoded_jwt


def verify_access_token(token: str) -> dict:
    """Verifica y decodifica un token de acceso JWT."""
    try:
        payload = jwt.decode(token, os.getenv("SECRETE_KEY"), algorithms=[os.getenv("ALGORITHM")])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload
