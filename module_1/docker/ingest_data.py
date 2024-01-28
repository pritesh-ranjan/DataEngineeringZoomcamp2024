from time import time
import argparse
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table_name
    csv_url = params.url
    csv_out = "out.csv"
    
    download_and_decompress_file(csv_url, csv_out)

    ldf = pd.read_csv(csv_out, nrows=100)
    ldf.head()

    # make sure pandas recognize date time fields
    ldf.tpep_pickup_datetime = pd.to_datetime(ldf.tpep_pickup_datetime)
    ldf.tpep_dropoff_datetime = pd.to_datetime(ldf.tpep_dropoff_datetime)

    engine = create_engine(
        f'postgresql://{user}:{password}@{host}:{port}/{db}')

    schema = pd.io.sql.get_schema(ldf, name=table, con=engine)
    print(schema)

    # first only create table with n=0 and then insert
    ldf.head(n=0).to_sql(name=table,
                         con=engine, if_exists='replace')

    # load csv into iterator
    df_iter = pd.read_csv(csv_out,
                          iterator=True, chunksize=100000)

    for df in df_iter:
        t_start = time()

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table, con=engine, if_exists='append')

        t_end = time()
        print(f"inserted 100000 records in {-t_start+t_end: .3f} seconds")

def download_and_decompress_file(csv_url, csv_out):
    delete_if_exists(csv_out)
    os.system(f"wget {csv_url} -O {csv_out}.gz")
    os.system(f"gzip -d {csv_out}.gz")

def delete_if_exists(csv_out):
    Path(f"{csv_out}.gz").unlink(missing_ok=True)
    Path(csv_out).unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest csv data to postgres')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--host', help='host name for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument(
        '--table_name', help='table name for storing data in postgres')
    parser.add_argument('--url', help='url for csv')

    args = parser.parse_args()
    main(args)
