from psycopg2.extensions import cursor, connection
from sql_queries import (
    create_staging_table_queries,
    create_table_queries,
    drop_staging_table_queries,
    drop_table_queries,
)


def drop_staging_tables(cur: cursor, conn: connection) -> None:
    for table, query in drop_staging_table_queries:
        print(f"Dropping {table} table")
        cur.execute(query)
        conn.commit()


def drop_tables(cur: cursor, conn: connection) -> None:
    for table, query in drop_table_queries:
        print(f"Dropping {table} table")
        cur.execute(query)
        conn.commit()


def create_staging_tables(cur: cursor, conn: connection) -> None:
    for table, query in create_staging_table_queries:
        print(f"Creating {table} table")
        cur.execute(query)
        conn.commit()


def create_tables(cur: cursor, conn: connection) -> None:
    for table, query in create_table_queries:
        print(f"Creating {table} table")
        cur.execute(query)
        conn.commit()
