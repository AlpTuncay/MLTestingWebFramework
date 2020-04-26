from project.messaging import consumer, producer
import logging
import json
import os
from base64 import b64encode, b64decode
import shutil
import zipfile
import time
from datetime import datetime
import json


def parse_json_config(json):
    pass

if __name__ == '__main__':

    def on_msg_receive(ch, method, properties, body):
        received = json.loads(body)
        logging.error(" [X] Received test request %s" % received["model_id"])

        test_path = "./test/model/%s" % received["model_id"]

        if not os.path.exists(test_path):
            os.makedirs(test_path)

        # config_header, config_encoded = received["model_config"].split(",", 1)
        model_config_data = b64decode(received["model_config"])

        with open("%s/%s" % (test_path, received["model_config_filename"]), "wb+") as f:
            f.write(model_config_data)
        f.close()

        # test_data_header, test_data_encoded = received["test_data"].split(",", 1)
        test_data = b64decode(received["test_data"])

        with open("%s/%s" % (test_path, received["test_data_filename"]), "wb+") as f:
            f.write(test_data)
        f.close()

        compressed = zipfile.ZipFile("%s/%s" % (test_path, received["test_data_filename"]))
        compressed.extractall(test_path)

        test_config_data = b64decode(received["config_file"])

        with open("%s/%s" % (test_path, received["config_filename"]), "wb+") as f:
            f.write(test_config_data)
        f.close()

        with open("%s/%s" % (test_path, received["config_filename"]), "r") as f:
            config = json.load(f)
        f.close()

        response = {}
        # RUN THE TESTS HERE AND DELETE THE DATA AND THE MODEL CONFIG FILES
        if received["framework"] == "Keras":
            import keras
            from keras.models import load_model
            from keras.preprocessing.image import ImageDataGenerator

            model = load_model(test_path + "/" + received["model_config_filename"])

            if config["data_type"] == "image":
                img_data_gen_args = config["image_data_generator_args"]
                flow_from_dir_args = config["flow_from_directory_args"]

                try:

                    rescale_to_float = img_data_gen_args["rescale"].split("/")
                    rescale = float(rescale_to_float[0])/float(rescale_to_float[1])

                    test_gen = ImageDataGenerator(rescale=rescale)

                    generator = test_gen.flow_from_directory(test_path + "/data", **flow_from_dir_args)

                    start_time = time.time()
                    eval_result = model.evaluate_generator(generator)
                    elapsed_time = time.time() - start_time

                    response = {
                        "message": "Successfully loaded model",
                        model.metrics_names[0]: eval_result[0],
                        model.metrics_names[1]: eval_result[1],
                        "test_time": start_time,
                        "duration": elapsed_time,
                        "model_id": received["model_id"]
                    }

                except Exception as e:
                    response = {
                        "message": "Error occurred.",
                        "exception": str(e)
                    }
            elif config["data_type"] == "csv":
                import numpy as np
                # import pandas as pd
                from numpy import loadtxt
                data_file = os.listdir(test_path + "/data")[0]
                test_data = loadtxt(test_path + "/data/" + data_file, delimiter=",")

                y = test_data[:, config["target"]]
                X = np.delete(test_data, config["target"], axis=1)

                start_time = time.time()
                eval_result = model.evaluate(X, y)
                elapsed_time = time.time() - start_time

                response = {
                    "message": "Successfully loaded model",
                    model.metrics_names[0]: eval_result[0],
                    model.metrics_names[1]: eval_result[1],
                    "test_time": start_time,
                    "duration": elapsed_time,
                    "model_id": received["model_id"]
                }

        elif received["framework"] == "Sklearn":
            pass
        elif received["framework"] == "Tensorflow":
            pass
        elif received["framework"] == "PyTorch":
            pass

        response_producer = producer.Producer()

        response_producer.produce(json.dumps(response))

        shutil.rmtree("./test/model/%s" % received["model_id"])


    request_consumer = consumer.Consumer(callback=on_msg_receive)

    request_consumer.consume()
