"""Modulo de configuracion de variables de entorno"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Clase de configuracion de variables de entorno"""

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    DB_URL: str
    SECRETE_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    class Config:
        """Clase de configuracion de pydantic"""

        env_file = ".env"


settings = Settings()
