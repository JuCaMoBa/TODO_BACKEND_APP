""" Modelo que genera el esquema para la actualizacion de usuarios """

from pydantic import BaseModel, Field
from typing import Optional


class UserUpdate(BaseModel):
    """Esquema para la actualizacion de usuarios."""
    is_active: Optional[bool] = Field(None, description="Estado activo del usuario")
