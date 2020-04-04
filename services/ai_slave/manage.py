# from flask.cli import FlaskGroup
# from project import create_app
#
# app = create_app()
# cli = FlaskGroup(create_app=create_app)
#
#
# if __name__ == '__main__':
#     cli()
from project.messaging import consumer, producer
import logging
import json
import os
from base64 import b64encode, b64decode


if __name__ == '__main__':

    def on_msg_receive(ch, method, properties, body):
        received = json.loads(body)
        logging.error(" [X] Received test request %s" % received["model_id"])

        test_path = "./test/model/%s" % received["model_id"]

        if not os.path.exists(test_path):
            os.makedirs(test_path)

        # config_header, config_encoded = received["model_config"].split(",", 1)
        config_data = b64decode(received["model_config"])

        with open("%s/%s" % (test_path, received["model_config_filename"]), "wb+") as f:
            f.write(config_data)
        f.close()

        # test_data_header, test_data_encoded = received["test_data"].split(",", 1)
        test_data = b64decode(received["test_data"])

        with open("%s/%s" % (test_path, received["test_data_filename"]), "wb+") as f:
            f.write(test_data)
        f.close()

        # RUN THE TESTS HERE AND DELETE THE DATA AND THE MODEL CONFIG FILES

        response_producer = producer.Producer()

        response_producer.produce("Test response sent from AI Slave")


    request_consumer = consumer.Consumer(callback=on_msg_receive)

    request_consumer.consume()
