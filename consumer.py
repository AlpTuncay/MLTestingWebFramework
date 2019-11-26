import pika
import os


class Consumer:

    def __init__(self, host, queue, port, exchange):
        self.host = host
        self.queue = queue
        self.port = port
        self.exchange = exchange

        username = "user"
        password = "bitnami"

        credentials = pika.PlainCredentials(username, password)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port,
                                                                            virtual_host="/", credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, passive=True)

    def on_message(self, ch, method, properties, body):
        print(f"Data Received: {body}, Routing key: {method.routing_key}, {method.delivery_tag}")
        # with open("received_messages.txt", "a") as f:
        #     f.write(body + "\n")
        #     f.close()
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        print(f"Consumer starting")
        self.channel.basic_consume(self.on_message, self.queue)
        try:
            print(f"Started consumption")
            self.channel.start_consuming()
        except:
            print(f"Stopping consumption")
            self.channel.stop_consuming()
        # print(f"Connection closed")
        # self.connection.close()


if __name__ == '__main__':

    consumer = Consumer(host="localhost", queue="register-service-queue", port="5672", exchange="amq.direct")

    consumer.consume()
