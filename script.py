import requests
import csv
import os
import time
from os.path import join, dirname
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]

script_dir = dirname(__file__) 
dotenv_path = join(script_dir, '.env') 
load_dotenv(dotenv_path=dotenv_path)

import snowflake.connector as snowflake
from datetime import datetime

print(f"DEBUG Check 1: SNOWFLAKE_ACCOUNT from os.getenv is: {os.getenv('SNOWFLAKE_ACCOUNT')}")


POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')

LIMIT = 1000
DATE = '2025-09-26'

def run_stock_job():
    DATE = datetime.now().strftime('%Y-%m-%d')
    url =  f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    tickers = []

    data = response.json()
    for ticker in data['results']:
        ticker['date_stamp'] = DATE
        tickers.append(ticker)
    
    while "next_url" in data:
        print('requesting next page', data['next_url'])
        time.sleep(15)  # wait 15 seconds between requests
        response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
        data = response.json()
        #print(data)
        for ticker in data['results']:
            ticker['date_stamp'] = DATE
            tickers.append(ticker)
        
    #print(len(tickers))      

    example_ticker =  {
        'ticker': 'ZWS', 
	    'name': 'Zurn Elkay Water Solutions Corporation', 
	    'market': 'stocks', 
	    'locale': 'us', 
	    'primary_exchange': 'XNYS', 
	    'type': 'CS', 
	    'active': True, 
	    'currency_name': 'usd',
	    'cik': '0001439288',
	    'composite_figi': 'BBG000H8R0N8',
        'share_class_figi': 'BBG001T36GB5',
        'last_updated_utc': '2025-09-11T06:11:10.586204443Z',
        'date_stamp' : '2025-09-26'
    }

    fieldnames = list(example_ticker.keys())

    # Load to Snowflake instead of CSV
    load_to_snowflake(tickers, fieldnames)
    print(f'Loaded {len(tickers)} rows to Snowflake')



    # Write to CSV
    # output_csv = 'tickers.csv'

    # with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for t in tickers:
    #         row = {k: t.get(k, None) for k in fieldnames}
    #         writer.writerow(row)

    # print(f"✅ Wrote {len(tickers)} rows to {output_csv}")


def load_to_snowflake(rows, fieldnames):
    # Build connection kwargs from environment variables
    connect_kwargs = {
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
    }
    account = os.getenv('SNOWFLAKE_ACCOUNT')
    if account:
        connect_kwargs['account'] = account

    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    database = os.getenv('SNOWFLAKE_DATABASE')
    schema = os.getenv('SNOWFLAKE_SCHEMA')
    role = os.getenv('SNOWFLAKE_ROLE')
    if warehouse:
        connect_kwargs['warehouse'] = warehouse
    if database:
        connect_kwargs['database'] = database
    if schema:
        connect_kwargs['schema'] = schema
    if role:
        connect_kwargs['role'] = role

    print(connect_kwargs)

    conn = snowflake.connect( 
        user=connect_kwargs.get('user'),
        password=connect_kwargs.get('password'),
        account=connect_kwargs.get('account'),
        warehouse=connect_kwargs.get('warehouse'),
        database=connect_kwargs.get('database'),
        schema=connect_kwargs.get('schema'),
        role=connect_kwargs.get('role'),
        session_parameters={
        "CLIENT_TELEMETRY_ENABLED": False,
        }
    )


    try:
        cs = conn.cursor()
        try:
            table_name = os.getenv('SNOWFLAKE_TABLE', 'stock_tickers')

            # Define typed schema based on example_ticker
            type_overrides = {
                'ticker': 'VARCHAR',
                'name': 'VARCHAR',
                'market': 'VARCHAR',
                'locale': 'VARCHAR',
                'primary_exchange': 'VARCHAR',
                'type': 'VARCHAR',
                'active': 'BOOLEAN',
                'currency_name': 'VARCHAR',
                'cik': 'VARCHAR',
                'composite_figi': 'VARCHAR',
                'share_class_figi': 'VARCHAR',
                'last_updated_utc': 'TIMESTAMP_NTZ',
                'date_stamp': 'VARCHAR'
            }
            columns_sql_parts = []
            for col in fieldnames:
                col_type = type_overrides.get(col, 'VARCHAR')
                columns_sql_parts.append(f'"{col.upper()}" {col_type}')

            create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ( ' + ', '.join(columns_sql_parts) + ' )'
            cs.execute(create_table_sql)

            column_list = ', '.join([f'"{c.upper()}"' for c in fieldnames])
            placeholders = ', '.join([f'%({c})s' for c in fieldnames])
            insert_sql = f'INSERT INTO {table_name} ( {column_list} ) VALUES ( {placeholders} )'

            # Conform rows to fieldnames
            transformed = []
            for t in rows:
                row = {}
                for k in fieldnames:
                    row[k] = t.get(k, None)
                print(row)
                transformed.append(row)

            if transformed:
                cs.executemany(insert_sql, transformed)
        finally:
            cs.close()
    finally:
        conn.close()


if __name__ == '__main__':
    run_stock_job()