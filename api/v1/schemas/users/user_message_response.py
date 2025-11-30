"""Modulo ue genera la respuesta cuando se crea un usuario"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class UserMessageResponse(BaseModel):
    """Modelo de datos para la respuesta de un usuario"""
    success: bool = Field(..., title="Indica si la operacion fue exitosa")
    data: Optional[Any] = Field(None, title="Datos del usuario creado")
    message: str = Field(..., title="Mensaje de respuesta")
    status: int = Field(..., title="Codigo de estado HTTP")
