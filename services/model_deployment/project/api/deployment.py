from flask import Blueprint, request, jsonify, send_from_directory
from project import database
from sqlalchemy import exc
from project.api.models import ModelDefinition
from werkzeug.utils import secure_filename
import os
from base64 import b64encode, b64decode
import shutil
import logging

model_blueprint = Blueprint("models", __name__)


@model_blueprint.route("/models", methods=["POST"])
def deploy_model():
    model_title = request.json["data"]["model_title"]
    deployed_by = request.json["data"]["deployed_by"]
    model_framework = request.json["data"]["model_framework"]
    model_file = request.json["files"]["model_file"]
    custom_objects_file = request.json["files"]["custom_objects_file"] if "custom_objects_file" in request.json["files"] else None
    filename = request.json["filename"]
    custom_objects_filename = request.json["custom_objects_filename"] if "custom_objects_filename" in request.json else None

    model_definition = ModelDefinition(model_title=model_title, deployed_by=deployed_by, model_framework=model_framework, path_to_model="", path_to_custom_objects="")

    try:
        database.session.add(model_definition)
        database.session.flush()

        header, encoded = model_file.split(",", 1)
        data = b64decode(encoded)

        path_to_model = f"./user/{deployed_by}/models/{model_definition.id}/{model_framework}"

        if not os.path.exists(path_to_model):
            os.makedirs(path_to_model)

        with open(f"{path_to_model}/{filename}", "wb+") as f:
            f.write(data)

        if custom_objects_file:
            header, encoded = custom_objects_file.split(",", 1)
            data = b64decode(encoded)

            with open(f"{path_to_model}/{custom_objects_filename}", "wb+") as f:
                f.write(data)

            model_definition.path_to_custom_objects = f"{path_to_model}/{custom_objects_filename}"

        model_definition.path_to_model = f"{path_to_model}/{filename}"

        database.session.commit()

        response = {
            "status": 201,
            "message": f"Deployed model successfully. Model: {model_definition.model_title}"
        }

        return jsonify(response), response["status"]

    except exc.IntegrityError:
        database.session.rollback()

        response = {
            "status": 500,
            "message": f"Error occurred while deploying model {model_definition.model_title}"
        }

        return jsonify(response), response["status"]

    # IDEA -> First store model information, such as title, deployed_by and framework,
    # and then create the file path for the model_file to be saved.
    # Structure for folder path -> /users/<id>/models/<framework>/<model_id>/<model_file>

@model_blueprint.route("/models/<model_id>", methods=["POST"])
def update_model(model_id):
    model_definition = ModelDefinition.query.filter_by(id=model_id).first()

    model_file = request.json["files"]
    filename = request.json["filename"]

    try:
        header, encoded = model_file.split(",", 1)
        data = b64decode(encoded)

        path_to_model = f"./user/{model_definition.deployed_by}/models/{model_id}/{model_definition.model_framework}"

        os.remove(model_definition.path_to_model)

        with open(f"{path_to_model}/{filename}", "wb+") as f:
            f.write(data)

        model_definition.path_to_model = f"{path_to_model}/{filename}"

        database.session.commit()

        response = {
            "status": 201,
            "message": f"Updated model successfully. Model: {model_definition.model_title}"
        }

        return jsonify(response), response["status"]

    except exc.IntegrityError:
        database.session.rollback()

        response = {
            "status": 500,
            "message": f"Error occurred while updating model {model_definition.model_title}"
        }

        return jsonify(response), response["status"]

@model_blueprint.route("/models/<model_id>/custom_objects", methods=["POST"])
def update_custom_objects(model_id):
    model_definition = ModelDefinition.query.filter_by(id=model_id).first()

    custom_objects_file = request.json["files"]
    custom_objects_filename = request.json["custom_objects_filename"]
    try:
        header, encoded = custom_objects_file.split(",", 1)
        data = b64decode(encoded)

        path_to_model = f"./user/{model_definition.deployed_by}/models/{model_definition.id}/{model_definition.model_framework}"

        if model_definition.path_to_custom_objects:
            os.remove(model_definition.path_to_custom_objects)

        with open(f"{path_to_model}/{custom_objects_filename}", "wb+") as f:
            f.write(data)

        model_definition.path_to_custom_objects = f"{path_to_model}/{custom_objects_filename}"

        database.session.commit()

        response = {
            "status": 200,
            "message": f"Updated custom objcets successfully. Model: {model_definition.model_title}"
        }

        return jsonify(response), response["status"]

    except exc.IntegrityError:
        database.session.rollback()

        response = {
            "status": 500,
            "message": f"Error occurred while updating custom objects {model_definition.model_title}"
        }

        return jsonify(response), response["status"]

@model_blueprint.route("/models/all", methods=["GET"])
def get_all_models():
    models = ModelDefinition.query.all()

    if not models:
        response = {
            "status": 404,
            "message": "Cannot fetch models"
        }
        return jsonify(response), response["status"]
    else:
        response = {
            "status": 200,
            "message": "Successfully fetched models",
            "data": [model.to_json() for model in models]
        }
        return jsonify(response), response["status"]


@model_blueprint.route("/models/<model_id>", methods=["GET"])
def get_one_model(model_id):
    model = ModelDefinition.query.filter_by(id=model_id).first()

    if not model:
        response = {
            "status": 404,
            "message": "Cannot find model definition."
        }
        return jsonify(response), response["status"]
    else:
        response = {
            "status": 200,
            "message": "Fetched model successfully.",
            "data": model.to_json()
        }
        return jsonify(response), response["status"]


@model_blueprint.route("/user/models/<user_id>")
def get_model_by_user(user_id):
    models = ModelDefinition.query.filter_by(deployed_by=user_id).all()

    if not models:
        response = {
            "status": 404,
            "data": []
        }
        return jsonify(response), response["status"]
    else:
        response = {
            "status": 200,
            "message": "Successfully fetched models",
            "data": [model.to_json() for model in models]
        }
        return jsonify(response), response["status"]


@model_blueprint.route("/models/config/<model_id>", methods=["GET"])
def send_model_config(model_id):
    model = ModelDefinition.query.filter_by(id=model_id).first()

    if model:

        with open(model.path_to_model, "rb") as f:
            encoded_model = b64encode(f.read())
        f.close()

        response = {
            "config": encoded_model.decode(),
            "framework": model.model_framework,
            "filename": model.to_json()["filename"],
            "status": 200
        }

        if model.path_to_custom_objects:
            with open(model.path_to_custom_objects, "rb") as f:
                encoded_custom_objects = b64encode(f.read())
            f.close()

            response["custom_objects_file"] = encoded_custom_objects.decode()
            response["custom_objects_filename"] = model.to_json()["custom_objects_filename"]

        return jsonify(response), response["status"]
    else:
        response = {
            "message": "Model not found",
            "status": 404
        }

        return jsonify(response), response["status"]
