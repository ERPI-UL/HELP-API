#!/bin/bash
set -e

# This script will create user and database

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER lltk PASSWORD '$DB_LLTK_PW';
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO lltk;
EOSQL
