"""Modulo que genera los modelos de datos para la creacion de tareas"""

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Modelo de datos para la creacion de una tarea"""
    title: str = Field(..., title="Titulo de la tarea", max_length=255)
    description: str = Field(None, title="Descripcion de la tarea", max_length=1000)
    completed: bool = Field(False, title="Estado de la tarea")
