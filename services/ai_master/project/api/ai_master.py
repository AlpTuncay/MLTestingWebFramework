from flask import Blueprint, jsonify, request
import requests
from project import database
from project.api.models import ModelState
import logging
from base64 import b64decode, b64encode
import os
from project.messaging import producer, consumer
import threading
import json
from pyrabbit.api import Client


ai_master_blueprint = Blueprint("ai", __name__)

response_consumer = consumer.Consumer()

threading.Thread(target=response_consumer.consume).start()

@ai_master_blueprint.route("/test/<model_id>", methods=["POST"])
def create_model_test_request(model_id):
    # Here, service would receive an HTTP request that contains necessary
    # information for testing. Then, it will configure that request into a
    # format that would be passed in a message queue.
    request_producer = producer.Producer()

    requester_id = request.json["data"]["user_id"]
    device = request.json["data"]["device"]

    try:
        model_config_response = requests.get(f"http://models:5000/models/config/{model_id}").json()

        data_provider_response = requests.get(f"http://data-provider:5000/model/file/{model_id}").json()

        config_path = f"./config/model/{model_id}"

        if not os.path.exists(config_path):
            response = {
                "status": 404,
                "message": "Could not find config file."
            }

            return jsonify(response), response["status"]

        config_file = os.listdir(config_path)[0]

        with(open(f"{config_path}/{config_file}", "rb")) as f:
            encoded = b64encode(f.read())

        test_request_object = {
            "model_id": model_id,
            "model_config": model_config_response["config"],
            "model_config_filename": model_config_response["filename"],
            "framework": model_config_response["framework"],
            "test_data": data_provider_response["data_file"],
            "test_data_filename": data_provider_response["filename"],
            "config_file": encoded.decode(),
            "config_filename": config_file,
            "requester_id": requester_id
        }

        if "custom_objects_file" in model_config_response:
            test_request_object["custom_objects_file"] = model_config_response["custom_objects_file"]
            test_request_object["custom_objects_filename"] = model_config_response["custom_objects_filename"]

        request_queue = "/test/request/{}".format(device)
        request_producer.produce(json.dumps(test_request_object), request_queue)

        response = {
            "message": "Test request queued.",
            "status": 200
        }

        return jsonify(response), response["status"]
    except Exception as e:
        response = {
            "message": f"Failed to queue request. Exception: {e}",
            "status": 500
        }

        return jsonify(response), response["status"]

@ai_master_blueprint.route("/test/config/<model_id>", methods=["GET", "POST"])
def provide_test_config(model_id):

    if request.method == "POST":
        config_file = request.json["data"]["config_file"]
        model_id = request.json["data"]["model_id"]
        filename = request.json["data"]["filename"]

        config_path = f"./config/model/{model_id}"

        if not os.path.exists(config_path):
            os.makedirs(config_path)

        header, encoded = config_file.split(",", 1)
        data = b64decode(encoded)

        with open(f"{config_path}/{filename}", "wb+") as f:
            f.write(data)

        response = {
            "status": 201,
            "message": "Config file has been saved.",
            "filename": filename
        }

        return jsonify(response), response["status"]
    elif request.method == "GET":
        config_path = f"./config/model/{model_id}"

        try:
            config_file = os.listdir(config_path)

            # if config_file:
            response = {
                "status": 200,
                "available_config": config_file[0]
            }

            return jsonify(response), response["status"]
        except :
            response = {
                "status": 404,
                "message": "No config file found."
            }

            return jsonify(response), response["status"]


@ai_master_blueprint.route("/devices", methods=["GET"])
def get_testing_devices():
    # This is the end-point which would get information of the connected test devices
    # and then publish them to users.
    cl = Client("rabbitmq-broker:15672", "admin", "admin")

    response = {
        "status": 200,
        "queues": [q["name"].split("/")[-1] for q in cl.get_queues() if "request" in q["name"]]
    }

    return jsonify(response), response["status"]
