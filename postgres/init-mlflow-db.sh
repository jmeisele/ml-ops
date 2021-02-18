#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER mlflow WITH PASSWORD 'metadata';
    CREATE DATABASE mlflowdb;
    GRANT ALL PRIVILEGES ON DATABASE mlflowdb TO mlflow;
EOSQL