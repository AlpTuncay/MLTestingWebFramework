import pika
import logging
import os
import subprocess


class Consumer:

    def __init__(self, callback):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq-broker", credentials=pika.PlainCredentials("admin", "admin"))
        )

        self.channel = self.connection.channel()

        # host_device_name = os.getenv("hostname")
        host_device_name = subprocess.check_output(["cat", "/usr/etc/hostname"]).decode("utf-8")
        host_device_name = ''.join(host_device_name.split())

        logging.error(host_device_name)

        self.queue = "/test/request/{}".format(host_device_name) # Should be different for each slave
        # self.queue = "test-request-queue"
        self.callback = callback

    def consume(self):
        self.channel.queue_declare(queue=self.queue, exclusive=True)

        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()
