"""Modulo que genera el modelo de datos para el mensaje de respuesta de una tarea"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class TaskMessageResponse(BaseModel):
    """Modelo de datos para la respuesta de una tarea"""
    success: bool = Field(..., title="Indica si la operacion fue exitosa")
    data: Optional[Any] = Field(None, title="Datos de la tarea")
    message: str = Field(..., title="Mensaje de respuesta")
    status: int = Field(..., title="Codigo de estado HTTP")
