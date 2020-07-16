#!/usr/bin/env sh

echo "Waiting for postgres"

while ! nc -z modelstate-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py create-db
python manage.py run -h 0.0.0.0
