import pika
import os
import time
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class Producer:

    def __init__(self, host, port, exchange):
        self.username = "user"
        self.password = "bitnami"
        self.host = host
        self.exchange = exchange
        self.port = port

        # credentials = pika.PlainCredentials(self.username, self.password)
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port,
        #                                                                virtual_host="/", credentials=credentials))

        # self.channel = self.connection.channel(self.on_channel_open)

        # self.connection = None
        # self.channel = None
        # self.stopping = False

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)

        return pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port,
                                                                       virtual_host="/", credentials=credentials))
    #
    # def on_connection_open(self):
    #     LOGGER.info("Connection opened")
    #
    # def on_connection_open_error(self):
    #     LOGGER.error("Connection open failed, retrying...")
    #     self.connection.ioloop.call_later(5, self.connection.ioloop.stop())
    #
    # def on_connection_closed(self):
    #     self.channel = None
    #     if self.stopping:
    #         self.connection.ioloop.stop()
    #     else:
    #         LOGGER.warning("Connection closed, reopening...")
    #         self.connection.ioloop.call_later(5, self.connection.ioloop.stop())
    #
    # def open_channel(self):
    #     LOGGER.info("Creating a new channel")
    #     self.connection.channel(on_open_callback=self.on_channel_open)
    #
    # def on_channel_open(self, channel):
    #     LOGGER.info('Channel opened')
    #     self._channel = channel
    #     # self._channel.add_on_close_callback(self.on_channel_closed)
    #
    # def on_channel_closed(self):
    #     LOGGER.warning("Channel closed")
    #     self.channel = None
    #     if not self.stopping:
    #         self.connection.close()
    #
    # def start_publishing(self):
    #     """This method will enable delivery confirmations and schedule the
    #     first message to be sent to RabbitMQ
    #     """
    #     LOGGER.info('Issuing consumer related RPC commands')
    #     self.channel.confirm_delivery()
    #     self.schedule_next_message()

    def produce_msg(self, msg):
        connection = None
        channel = None
        try:
            connection = self.connect()
            channel = connection.channel()
            print("Trying to publish")
            channel.exchange_declare(exchange=self.exchange, exchange_type="direct", passive=True)
            data = channel.basic_publish(exchange=self.exchange, body=msg, routing_key="service.register")
            print(f"Publishing is done.\nData:{data}")
        except Exception as e:
            print(e)
        finally:
            if connection:
                print("Closing connection")
                # channel.close()
                connection.close()


if __name__ == '__main__':

    producer = Producer(host="localhost", port="5672", exchange="amq.direct")

    i = 1

    # while i < 5:
    msg = "A Message no:%d from Producer to Consumer" % i
    msg = str.encode(msg)
    print(f"{msg} should have been sent.")
    producer.produce_msg(msg)

        # i += 1
        # time.sleep(5)


