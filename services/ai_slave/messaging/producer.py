import pika


class Producer:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq-broker"),
            pika.PlainCredentials("admin", "admin")
        )

        self.channel = self.connection.channel()

        self.queue = "test-response-queue"

    def produce(self, body):
        self.channel.queue_declare(queue=self.queue)

        self.channel.basic_publish(exchange="amq.topic", routing_key=self.queue, body=body)
        self.connection.close()
