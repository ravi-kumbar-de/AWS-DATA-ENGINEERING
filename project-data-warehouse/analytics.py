import configparser
import redshift_connector
from sql_queries import count_rows_queries, analytics_queries


def run_count_rows_queries(cur, conn):
    for i, query in enumerate(count_rows_queries):
        print(f'\t- Query {i+1}/{len(count_rows_queries)}')

        print('\t\t- Executing')
        print(query)
        cur.execute(query)
        results = cur.fetchall()
        
        for row in results:
            print("Number of rows", row)
        
        print('\n\n')


def run_analytics_queries(cur, conn):
    for i, item in enumerate(analytics_queries):
        print(f'\t- Query {i+1}/{len(analytics_queries)}')

        print(f'\t\t- {item["question"]}')
        cur.execute(item["query"])
        results = cur.fetchall()
        
        for row in results:
            print(row)
        
        print('\n\n')


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

    print('- Counting Number of Rows in Each Table')
    run_count_rows_queries(cur, conn)
    
    print('- Analytics')
    run_analytics_queries(cur, conn)

    print('- Closing connection')
    conn.close()


if __name__ == "__main__":
    main()