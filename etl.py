#!/usr/bin/env python3

import argparse
from psycopg2.extensions import cursor, connection

from settings import get_config
from db import get_connection
from create_tables import (
    drop_tables,
    create_tables,
    drop_staging_tables,
    create_staging_tables,
)
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
    parser = argparse.ArgumentParser(
        description="Sparkify ETL"
    )

    option_group = parser.add_mutually_exclusive_group(required=True)

    option_group.add_argument(
        "--create-tables",
        action="store_true",
        help="Create Tables",
    )

    option_group.add_argument(
        "--load-data",
        action="store_true",
        help="Load Data",
    )

    parser.add_argument(
        "--staging",
        action="store_true",
        default=False,
        help="Include Staging",
    )

    args = parser.parse_args()

    config = get_config()

    conn = get_connection(config["CLUSTER"])
    cur = conn.cursor()

    if args.create_tables:
        if args.staging:
            drop_staging_tables(cur, conn)
            create_staging_tables(cur, conn)
        drop_tables(cur, conn)
        create_tables(cur, conn)
    elif args.load_data:
        if args.staging:
            load_staging_tables(cur, conn)
        insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
