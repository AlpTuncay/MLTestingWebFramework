from flask import Blueprint, request, jsonify, send_from_directory
from project import database
from sqlalchemy import exc
from project.api.models import ProviderObject
import os
from base64 import b64encode, b64decode
import logging
import shutil


provider_blueprint = Blueprint("provider", __name__)


@provider_blueprint.route("/provider/upload", methods=["POST"])
def upload_test_data():
    data_file = request.json["data"]["data_file"]
    model_id = request.json["data"]["model_id"]
    filename = request.json["data"]["filename"]

    previous_provider_object = ProviderObject.query.filter_by(model_id=model_id).first()

    try:

        if not previous_provider_object:
            provider_object = ProviderObject(model_id=model_id, data_path="")


            database.session.add(provider_object)
            database.session.flush()

            header, encoded = data_file.split(",", 1)
            data = b64decode(encoded)

            data_path = f"./model/{model_id}/data/{provider_object.id}"

            if not os.path.exists(data_path):
                os.makedirs(data_path)

            with open(f"{data_path}/{filename}", "wb+") as f:
                f.write(data)

            provider_object.data_path = data_path + f"/{filename}"
            database.session.commit()

            response = {
                "status": 201,
                "message": f"Data upload successful. Data: {filename}"
            }

            return jsonify(response), response["status"]

        else:
            # Here update the current data_store entry with the new incoming data file
            existing_file_path = previous_provider_object.data_path
            os.remove(existing_file_path)

            data_path = f"./model/{model_id}/data/{previous_provider_object.id}"

            if not os.path.exists(data_path):
                os.makedirs(data_path)

            header, encoded = data_file.split(",", 1)
            data = b64decode(encoded)

            with open(data_path + f"/{filename}", "wb+") as f:
                f.write(data)

            previous_provider_object.data_path = data_path + f"/{filename}"

            database.session.commit()

            response = {
                "status": 200,
                "message": f"New data upload successful. Data: {filename}"
            }

            return jsonify(response), response["status"]

    except (exc.IntegrityError, Exception) as e:
        database.session.rollback()

        response = {
            "status": 500,
            "message": f"Error occurred while uploading data. Exception {e}"
        }

        return jsonify(response), response["status"]


@provider_blueprint.route("/model/<model_id>/data", methods=["GET"])
def get_test_data_by_model_id(model_id):
    provider_object = ProviderObject.query.filter_by(model_id=model_id).first()

    if not provider_object:
        response = {
            "status": 404,
            "message": "Cannot find data to provide for this model"
        }

        return jsonify(response), response["status"]

    else:
        response = {
            "status": 200,
            "message": "Fetched data succesfully.",
            "data": provider_object.to_json()
        }

        return jsonify(response), response["status"]

@provider_blueprint.route("/model/file/<model_id>", methods=["GET"])
def send_data_file(model_id):
    provider_object = ProviderObject.query.filter_by(model_id=model_id).first()

    if provider_object:
        with open(provider_object.data_path, "rb") as f:
            encoded = b64encode(f.read())
        f.close()

        response = {
            "data_file": encoded.decode(),
            "filename": provider_object.to_json()["filename"],
            "status": 200
        }

        return jsonify(response), response["status"]
    else:
        response = {
            "message": "Data file not found",
            "status": 404
        }

        return jsonify(response), response["status"]
