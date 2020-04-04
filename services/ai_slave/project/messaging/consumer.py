import pika
import logging


class Consumer:

    def __init__(self, callback):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq-broker")
        )

        self.channel = self.connection.channel()

        self.queue = "test-request-queue"

        self.callback = callback

    def consume(self):
        # self.channel.queue_declare(queue=self.queue, durable=True)

        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()
