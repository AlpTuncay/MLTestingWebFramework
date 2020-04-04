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

ai_master_blueprint = Blueprint("ai", __name__)

response_consumer = consumer.Consumer()

threading.Thread(target=response_consumer.consume).start()

@ai_master_blueprint.route("/test/<model_id>", methods=["GET"])
def create_model_test_request(model_id):
    # Here, service would receive an HTTP request that contains necessary
    # information for testing. Then, it will configure that request into a
    # format that would be passed in a message queue.
    request_producer = producer.Producer()

    try:
        model_config_response = requests.get(f"http://models:5000/models/config/{model_id}").json()

        data_provider_response = requests.get(f"http://data-provider:5000/model/file/{model_id}").json()

        test_request_object = {
            "model_id": model_id,
            "model_config": model_config_response["config"],
            "model_config_filename": model_config_response["filename"],
            "framework": model_config_response["framework"],
            "test_data": data_provider_response["data_file"],
            "test_data_filename": data_provider_response["filename"]
        }

        request_producer.produce(json.dumps(test_request_object))

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

@ai_master_blueprint.route("/test/devices", methods=["GET"])
def get_testing_devices():
    # This is the end-point which would get information of the connected test devices
    # and then publish them to users.
    pass
