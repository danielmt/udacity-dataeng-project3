from typing import Dict, Any

import psycopg2
from psycopg2.extensions import connection


def get_connection(config: Dict[str, Any]) -> connection:
    """connect to database and return a connection and cursor tuple"""

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            config["HOST"],
            config["DB_NAME"],
            config["DB_USER"],
            config["DB_PASSWORD"],
            config["DB_PORT"],
        )
    )

    return conn
