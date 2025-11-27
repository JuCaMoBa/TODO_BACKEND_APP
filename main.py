from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.global_config.global_config import get_deployment_enviroment


app = FastAPI(
    title="TODO API",
    version="0.1.0",
    docs_url=get_deployment_enviroment().docs_url,
    redoc_url=get_deployment_enviroment().redoc_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_deployment_enviroment().URL_ALLOWED_CORS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app)
