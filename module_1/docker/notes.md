# Introduction to docker

Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. It is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

While shipping applications in docker, we can include all the application code, configuration and dependencies into a container and can execute it any where.

Benefits:
1. Reproducibility
2. Local experiments
3. Integration test (CI/CD)
4. Running pipelines on the cloud
5. Version and update management
6. Spark
7. Serverless

If a container is corrupted or negatively impacted, it doesnot affect the host machines or other conatainer running in same host machine



Used Commands:

postgres: {urlstring: postgresql://root:root@localhost:5432/ny_taxi}
```bash
docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi"  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432 --network=pg-network --name pg-database postgres:13
```

pgAdmin:  
```bash
docker run -it -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" -e PGADMIN_DEFAULT_PASSWORD="root" -p 8080:80 --network=pg-network --name pg-admin2 dpage/pgadmin4
```
PGCLI: 
```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

Convert jupyter notebook to .py file: 
```bash
jupyter nbconvert --to=script ny_taxi.ipynb
```

URL: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz

python ingest_data.py --user=root --password=root --host=localhost --port=5432 --db=ny_taxi --table_name=yellow_taxi_trips --url=${URL}

docker build -t taxi_ingest:v01 .

docker run -it --network=pg-network taxi_ingest:v01 --user=root --password=root --host=pg-database --port=5432 --db=ny_taxi --table_name=yellow_taxi_trips --url=${URL}