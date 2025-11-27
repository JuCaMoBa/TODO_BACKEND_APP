"""Modulo que genera los modelos de datos para la creacion de usuarios"""

from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    """Modelo de datos para la creacion de un usuario"""
    username: str = Field(..., title="Nombre de usuario", max_length=50)
    email: EmailStr = Field(..., title="Correo electronico", max_length=100)
    password: str = Field(..., title="Contrasena", min_length=8, max_length=128)
    is_active: bool = Field(True, title="Estado del usuario")
