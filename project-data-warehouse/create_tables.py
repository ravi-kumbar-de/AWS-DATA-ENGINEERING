import configparser
import redshift_connector
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for i, query in enumerate(drop_table_queries):
        print(f'\t- Query {i+1}/{len(drop_table_queries)}')
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for i, query in enumerate(create_table_queries):
        print(f'\t- Query {i+1}/{len(create_table_queries)}')
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    print('- Connecting to the Cluster Database')
    conn = redshift_connector.connect(
        host=config['DWH']['DWH_ENDPOINT'],
        database=config['DWH']['DWH_DB'],
        port=config['DWH']['DWH_PORT'],
        user=config['DWH']['DWH_DB_USER'],
        password=config['DWH']['DWH_DB_PASSWORD']
    )

    cur = conn.cursor()

    print('- Dropping existing tables')
    drop_tables(cur, conn)

    print('- Creating tables')
    create_tables(cur, conn)

    print('- Closing connection')
    conn.close()


if __name__ == "__main__":
    main()
