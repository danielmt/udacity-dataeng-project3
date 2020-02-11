import psycopg2
from psycopg2.extensions import connection

from settings import get_config


def get_connection() -> connection:
    """connect to database and return a connection and cursor tuple"""

    config = get_config()
    cluster_config = config["CLUSTER"]

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            cluster_config.get("HOST"),
            cluster_config.get("DB_NAME"),
            cluster_config.get("DB_USER"),
            cluster_config.get("DB_PASSWORD"),
            cluster_config.get("DB_PORT"),
        )
    )

    return conn
