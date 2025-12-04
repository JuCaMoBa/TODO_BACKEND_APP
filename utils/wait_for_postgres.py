"""Utilidad para esperar a que PostgreSQL esté listo antes de continuar."""

import logging
import time
import psycopg2

logger = logging.getLogger("app")


def wait_for_postgres(db_url: str):
    for i in range(10):
        try:
            conn = psycopg2.connect(db_url)
            conn.close()
            logger.info("PostgreSQL está listo.")
            return
        except Exception as e:
            logger.warning(f"PostgreSQL no está listo todavía, reintentando... ({i+1}/10): {e}")
            time.sleep(2)

    raise Exception("PostgreSQL no se pudo iniciar.")
