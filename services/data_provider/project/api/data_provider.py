from flask import Blueprint, request, jsonify, send_from_directory
from project import database
from sqlalchemy import exc
from project.api.models import ProviderObject
import os
from base64 import b64encode, b64decode
import logging


provider_blueprint = Blueprint("provider", __name__)


@provider_blueprint.route("/provider/upload", methods=["POST"])
def upload_test_data():
    data_file = request.json["data"]["data_file"]
    model_id = request.json["data"]["model_id"]
    filename = request.json["data"]["filename"]

    provider_object = ProviderObject(model_id=model_id, data_path="")

    try:
        database.session.add(provider_object)
        database.session.flush()

        header, encoded = data_file.split(",", 1)
        data = b64decode(encoded)

        data_path = f"./model/{model_id}/data/{provider_object.id}"

        if not os.path.exists(data_path):
            os.makedirs(data_path)

        with open(data_path + f"/{filename}", "wb+") as f:
            f.write(data)

        provider_object.data_path = data_path + f"/{filename}"
        database.session.commit()

        response = {
            "status": 201,
            "message": f"Data upload successful. Data: {filename}"
        }

        return jsonify(response), response["status"]

    except (exc.IntegrityError, Exception) as e:
        database.session.rollback()

        response = {
            "status": 500,
            "message": f"Error occurred while uploading data. Exception {e}"
        }

@provider_blueprint.route("/provider/data/<data_id>", methods=["GET"])
def get_test_data_by_id(data_id):
    pass


@provider_blueprint.route("/provider/data/model/<model_id>", methods=["GET"])
def get_test_data_by_model_id(model_id):
    pass
