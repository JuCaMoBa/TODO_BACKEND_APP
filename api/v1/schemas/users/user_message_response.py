"""Modulo ue genera la respuesta cuando se crea un usuario"""

from pydantic import BaseModel, Field


class UserMessageResponse(BaseModel):
    """Modelo de datos para la respuesta de un usuario"""

    message: str = Field(..., title="Mensaje de respuesta")
    status: int = Field(..., title="Codigo de estado HTTP")
