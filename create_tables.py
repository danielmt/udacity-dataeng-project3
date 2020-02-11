#!/usr/bin/env python3

from psycopg2.extensions import cursor, connection

from db import get_connection
from sql_queries import (
    create_table_queries,
    drop_table_queries,
)


def drop_tables(cur: cursor, conn: connection) -> None:
    for table, query in drop_table_queries:
        print(f"Dropping {table} table")
        cur.execute(query)
        conn.commit()


def create_tables(cur: cursor, conn: connection) -> None:
    for table, query in create_table_queries:
        print(f"Creating {table} table")
        cur.execute(query)
        conn.commit()


def main():
    conn = get_connection()
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
