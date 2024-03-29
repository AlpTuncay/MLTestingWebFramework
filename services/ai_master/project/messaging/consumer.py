import pika
import logging
import requests
import json


class Consumer:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq-broker", credentials=pika.PlainCredentials("admin", "admin"))
        )

        self.channel = self.connection.channel()

        self.queue = "/test/response"

    def consume(self):
        self.channel.queue_declare(queue=self.queue)

        self.channel.basic_consume(queue=self.queue, on_message_callback=self._on_msg_receive, auto_ack=True)

        self.channel.start_consuming()

    def _on_msg_receive(self, ch, method, properties, body):
        # Here send request to the model_information service with the results
        # from ai_slave
        received = json.loads(body)
        logging.error(" [X] Received %r" % received)

        test_status = received["test_status"]
        model_id = received["model_id"]
        test_acc = received["accuracy"] if test_status == "Success" else 0.0
        test_loss = received["loss"] if test_status == "Success" else 0.0
        test_duration = received["duration"] if test_status == "Success" else 0.0
        reason = received["reason"] if test_status == "Fail" else None
        last_test_time = received["test_time"]
        requester_id = received["requester_id"]
        test_device = received["device"]

        logging.error(test_device)

        requests.post("http://model-info:5000/model_info", json={"data":{
                                                                        "model_id": model_id,
                                                                        "test_acc": test_acc,
                                                                        "test_loss": test_loss,
                                                                        "last_test_time": last_test_time,
                                                                        "test_duration": test_duration,
                                                                        "test_status": test_status,
                                                                        "test_device": test_device
                                                                    }})
        try:
            requests.post("http://mailer:5000/send", json={"data":{
                                                                    "requester_id": requester_id,
                                                                    "model_id": model_id,
                                                                    "test_acc": test_acc,
                                                                    "test_loss": test_loss,
                                                                    "last_test_time": last_test_time,
                                                                    "test_duration": test_duration,
                                                                    "test_status": test_status,
                                                                    "reason": reason,
                                                                    "test_device": test_device
                                                                }})
        except Exception as e:
            raise e
