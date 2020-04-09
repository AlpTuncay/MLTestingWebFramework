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
import shutil
import zipfile

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

        compressed = zipfile.ZipFile("%s/%s" % (test_path, received["test_data_filename"]))
        compressed.extractall(test_path)

        response = {}
        # RUN THE TESTS HERE AND DELETE THE DATA AND THE MODEL CONFIG FILES
        if received["framework"] == "Keras":
            import keras
            from keras.models import load_model
            from keras.preprocessing.image import ImageDataGenerator

            model = load_model(test_path + "/" + received["model_config_filename"])

            test_gen = ImageDataGenerator(rescale=1./255)

            generator = test_gen.flow_from_directory(test_path + "/data", target_size=(256, 256), class_mode="binary")

            eval_result = model.evaluate_generator(generator)

            response = {
                "message": "Successfully loaded model",
                "result_1": eval_result[0],
                "result_2": eval_result[1]
            }

        elif received["framework"] == "Sklearn":
            pass
        elif received["framework"] == "Tensorflow":
            pass
        elif received["framework"] == "PyTorch":
            pass

        response_producer = producer.Producer()

        response_producer.produce(json.dumps(response))

        # shutil.rmtree("./test/model/%s" % received["model_id"])


    request_consumer = consumer.Consumer(callback=on_msg_receive)

    request_consumer.consume()
