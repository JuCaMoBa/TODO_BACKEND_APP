"""Modulo que genera los modelos de datos para actualizacion de tareas"""

from pydantic import BaseModel, Field


class TaskUpdate(BaseModel):
    """Modelo de datos para la actualizacion de una tarea"""
    title: str = Field(None, title="Titulo de la tarea", max_length=255)
    description: str = Field(None, title="Descripcion de la tarea", max_length=1000)
    completed: bool = Field(None, title="Estado de la tarea")
