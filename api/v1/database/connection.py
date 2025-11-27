"""Modulo de conexion a la base de datos."""
import psycopg2


class DatabaseConnection:
    """Clase para manejar la conexion a la base de datos."""

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Establece la conexion a la base de datos con context manager."""
        self.connection = psycopg2.connect(self.db_url)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Cierra la conexion a la base de datos con context manager."""
        if self.connection:
            if exc_type:
                self.connection.rollback()
            else:
                self.connection.commit()

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
