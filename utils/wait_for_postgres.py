"""Utilidad para esperar a que PostgreSQL esté listo antes de continuar."""

import logging
import time
import psycopg2


def wait_for_postgres(db_url: str):
    for i in range(10):
        try:
            conn = psycopg2.connect(db_url)
            conn.close()
            logging.info("PostgreSQL está listo.")
            return
        except Exception as e:
            logging.warning(f"PostgreSQL no está listo todavía, reintentando... ({i+1}/10): {e}")
            time.sleep(2)

    raise Exception("PostgreSQL no se pudo iniciar.")
