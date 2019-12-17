import pika
import os
import logging

logging.basicConfig(level=logging.DEBUG)


class Consumer:

    def __init__(self):
        self.host = os.getenv("BROKER")
        self.queue = os.getenv("QUEUE")
        self.port = os.getenv("PORT")
        self.exchange = os.getenv("EXCHANGE")

        # username = os.getenv("RABBITMQ_USERNAME")
        # password = os.getenv("RABBITMQ_PASSWORD")

        # credentials = pika.PlainCredentials(username, password)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port,
                                                                            virtual_host="/"))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, passive=True)

    def on_message(self, ch, method, properties, body):
        logging.info(f"Data Received: {body}, Routing key: {method.routing_key}")
        with open("received_messages.txt", "a") as f:
            f.write(body.decode("utf-8") + "\n")
            f.close()
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        logging.info(f"Consumer starting")
        self.channel.basic_consume(self.queue, self.on_message, auto_ack=False)
        # try:
        logging.info(f"Started consumption")
        self.channel.start_consuming()
        # except:
        #     print(f"Stopping consumption")
        #     self.channel.stop_consuming()
        print(f"Connection closed")
        # self.connection.close()