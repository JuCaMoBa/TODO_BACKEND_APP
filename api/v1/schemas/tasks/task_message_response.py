"""Modulo que genera el modelo de datos para el mensaje de respuesta de una tarea"""

from pydantic import BaseModel, Field
from api.v1.schemas.tasks.task_response import TaskResponse


class TaskMessageResponse(BaseModel):
    """Modelo de datos para la respuesta de una tarea"""
    task: TaskResponse
    message: str = Field(..., title="Mensaje de respuesta")
    status: int = Field(..., title="Codigo de estado HTTP")
