import pika
import logging


class Consumer:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq-broker")
        )

        self.channel = self.connection.channel()

        self.queue = "test-response-queue"

    def consume(self):
        # self.channel.queue_declare(queue=self.queue, durable=True)

        self.channel.basic_consume(queue=self.queue, on_message_callback=self._on_msg_receive, auto_ack=True)

        self.channel.start_consuming()

    def _on_msg_receive(self, ch, method, properties, body):
        # Here send request to the model_information service with the results
        # from ai_slave
        logging.error(" [X] Received %r" % body)
