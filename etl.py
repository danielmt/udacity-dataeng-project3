#!/usr/bin/env python3

from psycopg2.extensions import cursor, connection

from db import get_connection
from sql_queries import (
    copy_table_queries,
    insert_table_queries
)


def load_staging_tables(cur: cursor, conn: connection) -> None:
    for table, query in copy_table_queries:
        print(f"Loading {table} data")
        cur.execute(query)
        conn.commit()


def insert_tables(cur: cursor, conn: connection) -> None:
    for table, query in insert_table_queries:
        print(f"Inserting data for {table} table")
        cur.execute(query)
        conn.commit()


def main():

    conn = get_connection()
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
