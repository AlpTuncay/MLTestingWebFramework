from flask import Blueprint, request, jsonify
from project import database
from sqlalchemy import exc
from project.api.models import ModelDefinition

model_blueprint = Blueprint("models", __name__)

@model_blueprint.route("/models", methods=["POST"])
def deploy_model():
    model_title = request.json["data"]["model_title"]
    deployed_by = request.json["data"]["deployed_by"]
    # File needs to be sent to the service


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
            "data": [model.to_json for model in models]
        }
        return jsonify(response), response["status"]