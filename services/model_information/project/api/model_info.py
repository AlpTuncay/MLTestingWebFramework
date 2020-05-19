from flask import Blueprint, request, jsonify
from project import database
from sqlalchemy import exc
from project.api.models import ModelState
from datetime import datetime
import logging

model_info_blueprint = Blueprint("model_info", __name__)


@model_info_blueprint.route("/model_info", methods=["POST"])
def create_state_instance():
    model_id = request.json["data"]["model_id"]
    test_accuracy = request.json["data"]["test_acc"]
    test_loss = request.json["data"]["test_loss"]
    last_test_time = request.json["data"]["last_test_time"]
    test_duration = request.json["data"]["test_duration"]
    test_status = request.json["data"]["test_status"]

    last_test_time = datetime.fromtimestamp(last_test_time)

    model_state = ModelState(model_id=model_id, test_accuracy=test_accuracy,
                            test_loss=test_loss, last_test_time=last_test_time,
                            test_duration=test_duration, test_status=test_status)

    try:
        database.session.add(model_state)
        database.session.commit()

        response = {
            "status": 201,
            "message": "Model state saved successfully"
        }

        return jsonify(response), response["status"]
    except exc.IntegrityError:
        database.session.rollback()

        response = {
            "status": 500,
            "message": "Error while saving model state."
        }

        return jsonify(response), response["status"]


@model_info_blueprint.route("/model_info/all", methods=["GET"])
def get_all_model_states():
    model_states = ModelState.query.all()

    if not model_states:
        response = {
            "status": 404,
            "message": "Cannot fetch model states."
        }

        return jsonify(response), response["status"]
    else:
        response = {
            "status": 200,
            "message": "Successfully fetched model states.",
            "data": [model_state.to_json() for model_state in model_states]
        }

        return jsonify(response), response["status"]


@model_info_blueprint.route("/state/<state_id>", methods=["GET"])
def get_one_state(state_id):
    model_state = ModelState.query.filter_by(id=state_id).first()
    try:
        if not model_state:
            response = {
                "status": 404,
                "message": "Cannot find model state."
            }

            return jsonify(response), response["status"]
        else:
            response = {
                "status": 200,
                "message": "Fetched model state successfully.",
                "data": model_state.to_json()
            }
    except Exception as e:
        response = {
            "status": 500,
            "message": f"Error occurred. {e}"
        }

        return jsonify(response), response["status"]


@model_info_blueprint.route("/model/info/<model_id>", methods=["GET"])
def get_latest_model_state(model_id):
    try:
        model_state = ModelState.query.filter_by(model_id=model_id).order_by(ModelState.id.desc()).first()

        if not model_state:
            response = {
                "status": 404,
                "message": "No model state found at this moment."
            }

            return jsonify(response), response["status"]
        else:
            response = {
                "status": 200,
                "message": "Successfully fetched model state.",
                "data": model_state.to_json()
            }

            return jsonify(response), response["status"]

    except Exception as e:
        response = {
            "status": 500,
            "message": f"Error occurred {e}"
        }

        return jsonify(response), response["status"]


@model_info_blueprint.route("/graph/<model_id>")
def get_graph_data_for_model(model_id):
    try:
        model_state_result = ModelState.query.filter_by(model_id=model_id).all()

        if not model_state_result:
            response = {
                "status": 404,
                "message": "No model state found at this moment."
            }

            return jsonify(response), response["status"]
        else:
            model_states = [state.to_json() for state in model_state_result]

            category = []

            acc_stats = []
            loss_stats = []

            for model_state in model_states:
                category.append({
                    "label": model_state["last_test_time"]
                })

                acc_stats.append({
                    "value": model_state["test_acc"]
                })

                loss_stats.append({
                    "value": model_state["test_loss"]
                })

            dataset = [
                {
                    "seriesname": "Accuracy",
                    "data": acc_stats
                },
                {
                    "seriesname": "Loss",
                    "data": loss_stats
                }
            ]

            response = {
                "status": 200,
                "graph_data": {
                    "category": category,
                    "dataset": dataset
                }
            }

            return jsonify(response), response["status"]

    except Exception as e:
        response = {
            "status": 500,
            "message": f"Error occurred {e}"
        }

        return jsonify(response), response["status"]

@model_info_blueprint.route("/", methods=["GET"])
def get_model_state_by_date():
    pass
