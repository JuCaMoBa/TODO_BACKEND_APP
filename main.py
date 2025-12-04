"""Archivo principal de la aplicación FastAPI."""

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


from contextlib import asynccontextmanager
from api.v1.models.tasks import create_tasks_tables
from api.v1.models.users import create_users_tables
from core.global_config.global_config import get_deployment_enviroment
from api.v1.routers.tasks_routes import router as tasks_router
from api.v1.routers.users_routes import router as users_router
from core.global_config.logging.logging_settings import log_config
from core.global_config.logging.logging import initialize_logging
from utils.wait_for_postgres import wait_for_postgres


initialize_logging()
logger = logging.getLogger("app")
logger.info("Iniciando la aplicación...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    wait_for_postgres(os.getenv("DB_URL"))
    create_users_tables(os.getenv("DB_URL"))
    create_tasks_tables(os.getenv("DB_URL"))
    logger.info("Tablas creadas o ya existentes.")

    yield

app = FastAPI(
    title="TODO API",
    version="0.1.0",
    docs_url=get_deployment_enviroment().docs_url,
    redoc_url=get_deployment_enviroment().redoc_url,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_deployment_enviroment().URL_ALLOWED_CORS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(users_router, prefix="/users", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_config=log_config, reload=False)
