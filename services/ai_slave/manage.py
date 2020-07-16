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
import psutil
import platform
import socket

def run_keras(config, test_path, received, start_time):
    import importlib.util
    from keras.models import load_model

    if "custom_objects_file" in received:
        custom_objects_file_path = test_path + "/" + received["custom_objects_filename"]

        spec = importlib.util.spec_from_file_location(os.path.splitext(received["custom_objects_filename"])[0], custom_objects_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for key in config["custom_objects"]:
            config["custom_objects"][key] = eval("%s.%s" % ("module", config["custom_objects"][key]))

        custom_objects = config["custom_objects"]
    else:
        custom_objects = None

    model = load_model(test_path + "/" + received["model_config_filename"], custom_objects=custom_objects)

    if config["data_type"] == "image":
        from keras.preprocessing.image import ImageDataGenerator

        img_data_gen_args = config["image_data_generator_args"]
        flow_from_dir_args = config["flow_from_directory_args"]

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

        try:
            if config["data_structure"] == "single":

                data_file = os.listdir(test_path + "/data")[0]
                test_data = np.genfromtxt(test_path + "/data/" + data_file, delimiter=",", skip_header = int(config["skip_rows"]) if "skip_rows" in config else 1)

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

def run_sklearn(config, test_path, received, start_time):
    from joblib import load
    import importlib
    from sklearn.metrics import log_loss
    import numpy as np

    try:
        model = load(test_path + "/" + received["model_config_filename"])
        scoring_module = importlib.import_module("sklearn.metrics")
        scoring_function = getattr(scoring_module, config["score_function"])
        if config["data_type"] == "csv":
            if config["data_structure"] == "single":

                data_file = os.listdir(test_path + "/data")[0]
                test_data = np.genfromtxt(test_path + "/data/" + data_file, delimiter=",", skip_header = int(config["skip_rows"]) if "skip_rows" in config else 1)
                logging.error(test_data)
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
        raise e
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

        if "custom_objects_file" in received:
            custom_objects_file = b64decode(received["custom_objects_file"])

            with open("%s/%s" % (test_path, received["custom_objects_filename"]), "wb+") as f:
                f.write(custom_objects_file)
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
            config = json.loads(f.read())
        f.close()

        # RUN THE TESTS HERE AND DELETE THE DATA AND THE MODEL CONFIG FILES
        start_time = time.time()
        try:
            if received["framework"] == "Keras":
                response = run_keras(config, test_path, received, start_time)
            elif received["framework"] == "Sklearn":
                response = run_sklearn(config, test_path, received, start_time)
            elif received["framework"] == "Tensorflow":
                pass
            elif received["framework"] == "PyTorch":
                pass
        except Exception as e:
            response = {
                "model_id": received["model_id"],
                "test_time": start_time,
                "reason": str(e),
                "test_status": "Fail"
            }

        response["requester_id"] = received["requester_id"]

        response_producer = producer.Producer()

        response_producer.produce(json.dumps(response))

        shutil.rmtree("./test/model/%s" % received["model_id"])

    request_consumer = consumer.Consumer(callback=on_msg_receive)

    request_consumer.consume()
