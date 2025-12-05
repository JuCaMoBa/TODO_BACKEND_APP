"""Modulo de esquema de token de autenticacion."""

from pydantic import BaseModel
from typing import Optional


class UserAuthData(BaseModel):
    """Esquema de datos para un usuario autenticado"""
    username: Optional[str] = None
    email: Optional[str] = None
    user_id: Optional[int] = None
    is_active: Optional[bool] = None


class Token(BaseModel):
    """Esquema de datos para el token"""
    access_token: str
    token_type: str
