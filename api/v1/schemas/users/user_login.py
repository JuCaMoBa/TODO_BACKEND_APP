"""Modulo que genera el modelo de datos para el login de usuarios"""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserLogin(BaseModel):
    """Modelo de datos para el login de un usuario"""
    username: Optional[str] = Field(..., title="Nombre de usuario", max_length=50)
    email: Optional[EmailStr] = Field(..., title="Correo electronico", max_length=100)
    password: str = Field(..., title="Contrasena", min_length=8, max_length=128)
