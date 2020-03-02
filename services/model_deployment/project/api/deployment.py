from flask import Blueprint, request, jsonify
from project import database
from sqlalchemy import exc
from project.api.models import ModelDefinition
from werkzeug.utils import secure_filename
import os
from base64 import b64decode


model_blueprint = Blueprint("models", __name__)


@model_blueprint.route("/models", methods=["POST"])
def deploy_model():
    model_title = request.json["data"]["model_title"]
    deployed_by = request.json["data"]["deployed_by"]
    model_framework = request.json["data"]["model_framework"]
    model_file = request.json["files"]
    filename = request.json["filename"]

    model_definition = ModelDefinition(model_title=model_title, deployed_by=deployed_by, model_framework=model_framework, path_to_model="")

    try:
        database.session.add(model_definition)
        database.session.flush()

        header, encoded = model_file.split(",", 1)
        data = b64decode(encoded)

        path_to_model = f"./user/{deployed_by}/models/{model_definition.id}/{model_framework}"

        if not os.path.exists(path_to_model):
            os.makedirs(path_to_model)

        with open(path_to_model + f"/{filename}", "wb+") as f:
            f.write(data)

        # model_file.save(path_to_model)

        model_definition.path_to_model = path_to_model + f"/{filename}"
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
            "data": [model.to_json for model in models]
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
