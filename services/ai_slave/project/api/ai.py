from flask import Blueprint, jsonify, request
import requests
from project import database
from project.api.models import ModelState
import logging
from base64 import b64decode, b64encode
import os
from project.messaging import consumer

# ai_blueprint = Blueprint("ai", __name__)

def listen_queue():
    request_consumer = consumer.Consumer()

    request_consumer.consume()

if __name__ == '__main__':
    listen_queue()

# @ai_blueprint.route("/test/<model_id>", methods=["GET"])
# def run_test_for_model(model_id):
#     try:
#         model_definition = requests.get(f"http://models:5000/models/{model_id}").json()
#
#         # logging.error("Config file: " + model_config_file)
#
#         config_file_path = os.path.dirname(model_definition["data"]["path"])
#
#         if not os.path.exists(config_file_path):
#             os.makedirs(config_file_path)
#
#             model_config_file = requests.get(f"http://models:5000/models/config/{model_id}").json()
#
#             with open(config_file_path + f"/{model_definition['data']['filename']}", "wb+") as f:
#                 f.write(b64decode(model_config_file["config"]))
#             f.close()
#
#         if model_definition["data"]["model_framework"] == "Keras":
#             from keras.models import load_model
#
#             # Do keras stuff here
#             model = load_model(config_file_path + f"/{model_definition['data']['filename']}")
#
#             model.summary()
#
#             response = {
#                 "message":  "Loaded",
#                 "status": 200
#             }
#
#             return jsonify(response), response["status"]
#
#         elif model_definition["data"]["model_framework"] == "Sklearn":
#             import sklearn
#             # Do sklearn stuff here
#             pass
#
#     except Exception as e:
#         response = {
#             "status": 500,
#             "message": "Error occurred. {}".format(e)
#         }
#         logging.exception(e)
#         return jsonify(response), response["status"]
