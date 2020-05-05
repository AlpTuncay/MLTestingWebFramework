from messaging import consumer, producer
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

def run_keras(config, test_path, received):
    import keras
    from keras.models import load_model
    from keras.preprocessing.image import ImageDataGenerator

    model = load_model(test_path + "/" + received["model_config_filename"])

    if config["data_type"] == "image":
        img_data_gen_args = config["image_data_generator_args"]
        flow_from_dir_args = config["flow_from_directory_args"]

        start_time = time.time()
        try:

            rescale_to_float = img_data_gen_args["rescale"].split("/")
            rescale = float(rescale_to_float[0])/float(rescale_to_float[1])

            test_gen = ImageDataGenerator(rescale=rescale)

            generator = test_gen.flow_from_directory(test_path + "/data", **flow_from_dir_args)

            eval_result = model.evaluate_generator(generator)
            elapsed_time = time.time() - start_time

            response = {
                model.metrics_names[0]: eval_result[0],
                model.metrics_names[1]: eval_result[1],
                "test_time": start_time,
                "duration": elapsed_time,
                "model_id": received["model_id"],
                "test_status": "Success"
            }

        except Exception as e:
            response = {
                "model_id": received["model_id"],
                "test_time": start_time,
                "reason": str(e),
                "test_status": "Fail"
            }

    elif config["data_type"] == "csv":
        import numpy as np
        import pandas as pd

        start_time = time.time()
        try:
            if config["data_structure"] == "single":

                data_file = os.listdir(test_path + "/data")[0]
                test_dataframe = pd.read_csv(test_path + "/data/" + data_file, header=None)
                test_data = test_dataframe.values

                y = test_data[:, config["target"]]
                X = np.delete(test_data, config["target"], axis=1)

                eval_result = model.evaluate(X, y)
                elapsed_time = time.time() - start_time

            elif config["data_structure"] == "folder":
                pass

            response = {
                model.metrics_names[0]: eval_result[0],
                model.metrics_names[1]: eval_result[1],
                "test_time": start_time,
                "duration": elapsed_time,
                "model_id": received["model_id"],
                "test_status": "Success"
            }
        except Exception as e:
            response = {
                "model_id": received["model_id"],
                "test_time": start_time,
                "reason": str(e),
                "test_status": "Fail"
            }

    return response

def run_sklearn(config, test_path, received):
    from joblib import load
    import importlib
    from sklearn.metrics import log_loss
    import pandas as pd
    import numpy as np

    start_time = time.time()
    try:
        model = load(test_path + "/" + received["model_config_filename"])
        scoring_module = importlib.import_module("sklearn.metrics")
        scoring_function = getattr(scoring_module, config["score_function"])
        if config["data_type"] == "csv":
            if config["data_structure"] == "single":

                data_file = os.listdir(test_path + "/data")[0]
                test_dataframe = pd.read_csv(test_path + "/data/" + data_file, header=None)
                test_data = test_dataframe.values

                y = list(test_data[:, config["target"]])
                X = list(np.delete(test_data, config["target"], axis=1))

                predictions = model.predict(X)
                score = scoring_function(y, predictions)
                loss_value = log_loss(y, predictions)
                elapsed_time = time.time() - start_time

            elif config["data_structure"] == "folder":
                pass

        elif config["data_type"] == "image":
            pass

        response = {
            "accuracy": score,
            "loss": loss_value,
            "test_time": start_time,
            "duration": elapsed_time,
            "model_id": received["model_id"],
            "test_status": "Success"
        }
    except Exception as e:
        response = {
            "model_id": received["model_id"],
            "test_time": start_time,
            "reason": str(e),
            "test_status": "Fail"
        }

    return response

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

        # RUN THE TESTS HERE AND DELETE THE DATA AND THE MODEL CONFIG FILES
        if received["framework"] == "Keras":
            response = run_keras(config, test_path, received)
        elif received["framework"] == "Sklearn":
            response = run_sklearn(config, test_path, received)
        elif received["framework"] == "Tensorflow":
            pass

        elif received["framework"] == "PyTorch":
            pass

        response_producer = producer.Producer()

        response_producer.produce(json.dumps(response))

        shutil.rmtree("./test/model/%s" % received["model_id"])


    request_consumer = consumer.Consumer(callback=on_msg_receive)

    request_consumer.consume()
