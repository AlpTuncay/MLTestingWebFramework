#!/usr/bin/env sh

while ! nc -z rabbitmq-broker 5672; do
 sleep 0.1
done

echo "RabbitMQ Broker started"

python3 manage.py run -h 0.0.0.0
