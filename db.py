from typing import Dict
import psycopg2
from psycopg2.extensions import connection


def get_connection(config: Dict[str, str]) -> connection:
    """connect to database and return a connection and cursor tuple"""

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            config.get("HOST"),
            config.get("DB_NAME"),
            config.get("DB_USER"),
            config.get("DB_PASSWORD"),
            config.get("DB_PORT"),
        )
    )

    return conn
