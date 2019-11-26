import pika
import os


class Producer:

    def __init__(self, host):
        self.host = host
        username = os.getenv("RABBITMQ_USERNAME")
        password = os.getenv("RABBITMQ_PASSWORD")
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, credentials=credentials))
        self.channel = self.connection.channel()
        # self.channel.queue_declare("register-service-queue")

    def produce_msg(self, msg):
        self.channel.basic_publish(body=msg, exchange="amq.direct", routing_key="service.register")
