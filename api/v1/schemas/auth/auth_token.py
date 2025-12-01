"""Modulo de esquema de token de autenticacion."""

from pydantic import BaseModel
from typing import Optional


class TokenData(BaseModel):
    """Esquema de datos de token de autenticacion."""
    username: Optional[str] = None
    email: Optional[str] = None
    user_id: Optional[int] = None
    is_active: Optional[bool] = None
