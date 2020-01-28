from psycopg2 import cursor, connection
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur: cursor, conn: connection) -> None:
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur: cursor, conn: connection) -> None:
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
