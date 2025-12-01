"""Modulo de dependencias de rutas API v1."""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from utils.auth_utils import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def current_user_dependency(token: Annotated[str, Depends(oauth2_scheme)]):
    """Dependencia para obtener el usuario actual."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)
    except Exception:
        raise credentials_exception
    return payload
