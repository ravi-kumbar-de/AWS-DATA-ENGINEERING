import configparser
import redshift_connector
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    for i, query in enumerate(copy_table_queries):
        print(f'\t- Query {i+1}/{len(copy_table_queries)}')

        print('\t\t- Executing')
        cur.execute(query)
        
        print('\t\t- Commiting')
        conn.commit()
        
        print('\t\t- Done')


def insert_tables(cur, conn):
    for i, query in enumerate(insert_table_queries):
        print(f'\t- Query {i+1}/{len(insert_table_queries)}')

        print('\t\t- Executing')
        cur.execute(query)

        print('\t\t- Commiting')
        conn.commit()

        print('\t\t- Done')


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

    print('- Loading Staging Tables')
    load_staging_tables(cur, conn)

    print('- Inserting Tables')
    insert_tables(cur, conn)

    print('- Closing connection')
    conn.close()


if __name__ == "__main__":
    main()