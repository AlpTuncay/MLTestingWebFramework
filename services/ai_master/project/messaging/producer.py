import pika


class Producer:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq-broker", credentials=pika.PlainCredentials("admin", "admin"))
        )

        self.channel = self.connection.channel()

    def produce(self, body, queue):

        self.channel.basic_publish(exchange="", routing_key=queue, body=body)
        self.connection.close()
