#!/usr/bin/env sh

echo "Waiting for postgres"

while ! nc -z models-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

#while ! nc -z rabbitmq-broker 5672; do
#  sleep 0.1
#done
#
#echo "RabbitMQ Broker started"

python manage.py run -h 0.0.0.0