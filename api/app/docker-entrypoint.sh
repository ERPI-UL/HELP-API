#!/bin/sh
echo $DB_HOST
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z database $SQL_DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#set -e
uvicorn main:app --port 5000 --host 0.0.0.0 --forwarded-allow-ips="*" 1>>logs.txt 2>&1
