from flask import Blueprint, jsonify, request
import requests
from project import database
from project.api.models import ModelState
import logging

ai_blueprint = Blueprint("ai", __name__)


@ai_blueprint.route("/test/<model_id>")
def run_test_for_model(model_id):
    try:
        model_definition = requests.get(f"http://models:5000/models/{model_id}").json()
        model_config_file = requests.get(f"http://models:5000/models/config/{model_id}")

        logging.error(f"File sent: %s" % model_config_file)

        if model_definition["data"]["model_framework"] == "Keras":
            from keras.models import load_model

            # Do keras stuff here
            pass

        elif model_definition["data"]["model_framework"] == "Sklearn":
            import sklearn
            # Do sklearn stuff here
            pass

    except Exception as e:
        response = {
            "status": 500,
            "message": "Error occurred. {}".format(e)
        }

        return jsonify(response), response["status"]


def preprocess_data():
    pass
