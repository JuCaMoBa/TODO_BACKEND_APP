"""Modulo de conexion a la base de datos."""

import atexit
from typing import Optional
from psycopg2.pool import ThreadedConnectionPool


class DatabaseConnection:
    """Clase para manejar la conexion a la base de datos."""

    _pool: Optional[ThreadedConnectionPool] = None

    def __init__(self, db_url: str, min_conn: int = 1, max_conn: int = 10):
        self.db_url = db_url
        self.min_conn = min_conn
        self.max_conn = max_conn
        self.connection = None
        self.cursor = None

        if DatabaseConnection._pool is None:
            DatabaseConnection._pool = ThreadedConnectionPool(
                minconn=self.min_conn,
                maxconn=self.max_conn,
                dsn=self.db_url
            )
            atexit.register(self._close_all_pool_connections)

    @classmethod
    def _close_all_pool_connections(cls):
        """Cierra todas las conexiones en el pool."""
        if cls._pool:
            cls._pool.closeall()
            cls._pool = None

    def __enter__(self):
        """Establece la conexion a la base de datos con pooling de conexiones."""
        self.connection = DatabaseConnection._pool.getconn()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Devuelve la conexión al pool."""
        if self.connection:
            if exc_type:
                self.connection.rollback()
            else:
                self.connection.commit()

        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            # Devuelve la conexion al pool
            DatabaseConnection._pool.putconn(self.connection)
            self.connection = None
