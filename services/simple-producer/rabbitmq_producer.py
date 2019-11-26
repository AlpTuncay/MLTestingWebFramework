import pika
import os
import logging



class Producer:

    def __init__(self):
        # self.username = os.getenv("RABBITMQ_USERNAME")
        # self.password = os.getenv("RABBITMQ_PASSWORD")
        self.host = os.getenv("BROKER")
        self.exchange = os.getenv("EXCHANGE")
        self.port = os.getenv("PORT")

        self.connection = self.connect()
        self.channel = self.connection.channel()

        logging.basicConfig(level=logging.DEBUG)

    def connect(self):
        # credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port,
                                                                       virtual_host="/"))

        return connection

    def produce_msg(self, msg):
        logging.info("In produce_message")
        # try:
        self.channel.exchange_declare(exchange=self.exchange, passive=True)
        logging.info("Trying to publish")

        data = self.channel.basic_publish(self.exchange, "service.register", msg,
                                     properties=pika.BasicProperties(delivery_mode=2))

        logging.info(f"Publishing is done.\nData:\n{data}")
        # finally:
        #     logging.info("Closing connection")
        #     self.connection.close()
        #     logging.info("Connection closed")

