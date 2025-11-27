"""Modulo que genera la respuesta cuando se consulta una tarea"""

from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    """Modelo de datos para la respuesta de una tarea"""
    id: int = Field(..., title="ID de la tarea")
    title: str = Field(..., title="Titulo de la tarea", max_length=255)
    description: str = Field(None, title="Descripcion de la tarea", max_length=1000)
    completed: bool = Field(False, title="Estado de la tarea")
