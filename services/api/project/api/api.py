from flask import Blueprint, request, current_app, jsonify
import requests
import logging
from functools import wraps
import jwt
from flask_cors import cross_origin
import os
from werkzeug.utils import secure_filename

views_blueprint = Blueprint("api", __name__)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            response = {
                "status": 401,
                "message": "Missing token."
            }
            return jsonify(response), 401

        try:
            token_decoded = jwt.decode(token, current_app.config.get("SECRET_KEY"))
            try:
                current_user = requests.get(f"http://register:5000/users/{token_decoded['sub']}").json()
                return func(current_user, *args, **kwargs)
            except requests.exceptions.ConnectionError:
                response = {
                    "status": 500,
                    "message": "Connection error occurred."
                }

                return jsonify(response), 500

        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.ExpiredSignatureError) as e:

            response = {
                "status": 401,
                "message": f"Invalid token {e}"
            }

            return jsonify(response), 401
    return decorated


@views_blueprint.route("/register", methods=["POST"])
@cross_origin()
def register_user():
    username = request.json["data"]["username"]
    email = request.json["data"]["email"]
    name = request.json["data"]["name"]
    surname = request.json["data"]["surname"]
    password = request.json["data"]["password"]

    try:
        r = requests.post("http://register:5000/users",
                      json={
                          "data": {
                              "username": username,
                              "email": email,
                              "name": name,
                              "surname": surname,
                              "password": password
                          }
                      })
        register_resp = r.json()

        return jsonify(register_resp), register_resp["status"]

    except requests.exceptions.ConnectionError:
        logging.error("Cannot post to register service")
        response = {
            "status": 500,
            "message": "Connection error occurred."
        }

        return jsonify(response), 500


@views_blueprint.route("/login", methods=["POST"])
@cross_origin()
def user_login():
    email = request.json["data"]["email"]
    password = request.json["data"]["password"]

    try:
        r = requests.post("http://login:5000/login", json={"data": {"email": email, "password": password}})
        login_resp = r.json()

        return jsonify(login_resp), login_resp["status"]
    except requests.exceptions.ConnectionError:
        logging.error("Cannot post to register service")
        response = {
            "status": 500,
            "message": "Connection error occurred."
        }
        return jsonify(response), 500

@views_blueprint.route("/user/profile", methods=["GET"])
@cross_origin()
@token_required
def profile(current_user):
    user_information = current_user["data"]
    user_id = user_information["id"]

    if current_user is not None:
        profile_response = {
            "user": user_information,
            "models": []
        }

        try:
            r = requests.get(f"http://models:5000/user/models/{user_id}")
            response = r.json()
            user_deployed_models = response["data"]
            profile_response["models"] = user_deployed_models
        except requests.exceptions.ConnectionError as e:
            profile_response["models"] = "Cannot connect to server right now."

        return jsonify(profile_response)
    else:
        response = {
            "status": 401,
            "message": "Login required"
        }

        return jsonify(response), response["status"]

@views_blueprint.route("/model/deploy", methods=["POST"])
@cross_origin()
@token_required
def deploy_model(current_user):

    # TODO Fix file upload issue
    model_title = request.json["data"]["model_title"]
    model_framework = request.json["data"]["model_framework"]
    model_file = request.json["files"]["model_file"]
    custom_objects_file = request.json["files"]["custom_objects_file"] if "custom_objects_file" in request.json["files"] else None
    filename = request.json["filename"]
    custom_objects_filename = request.json["custom_objects_filename"] if "custom_objects_filename" in request.json else None
    deployed_by = current_user["data"]["id"]

    try:
        r = requests.post("http://models:5000/models", json={"data": {"model_title": model_title,
                                                                      "model_framework": model_framework,
                                                                      "deployed_by": deployed_by}, "files":{"model_file": model_file, "custom_objects_file": custom_objects_file},
                                                                      "filename": filename, "custom_objects_filename": custom_objects_filename})
        response = r.json()

        return jsonify(response), response["status"]
    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]


@views_blueprint.route("/model/update/<model_id>", methods=["POST"])
@cross_origin()
@token_required
def update_model(current_user, model_id):
    model_file = request.json["files"]
    filename = request.json["filename"]

    try:
        r = requests.post(f"http://models:5000/models/{model_id}", json={"files": model_file, "filename": filename})
        response = r.json()

        return jsonify(response), response["status"]
    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]


@views_blueprint.route("/models/<model_id>", methods=["GET"])
@cross_origin()
@token_required
def fetch_model_info(current_user, model_id):
    try:
        r = requests.get(f"http://models:5000/models/{model_id}")
        response = r.json()

        return jsonify(response), response["status"]
    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]


@views_blueprint.route("/model/info/<model_id>", methods=["GET"])
@cross_origin()
@token_required
def fetch_model_state(current_user, model_id):
    try:
        r = requests.get(f"http://model-info:5000/model/info/{model_id}")

        response = r.json()

        return jsonify(response), response["status"]

    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]


@views_blueprint.route("/data/upload", methods=["POST"])
@cross_origin()
@token_required
def upload_data(current_user):
    data_file = request.json["data"]["data_file"]
    model_id = request.json["data"]["model_id"]
    filename = request.json["data"]["filename"]

    try:
        r = requests.post("http://data-provider:5000/provider/upload", json={
                          "data": {"data_file": data_file, "model_id": model_id, "filename": filename}
                          })

        response = r.json()

        return jsonify(response), response["status"]

    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]


@views_blueprint.route("/test/config", methods=["POST"])
@cross_origin()
@token_required
def upload_config(current_user):
    data_file = request.json["data"]["config_file"]
    model_id = request.json["data"]["model_id"]
    filename = request.json["data"]["filename"]

    try:
        r = requests.post(f"http://ai-master:5000/test/config/{model_id}", json={
                          "data": {"config_file": data_file, "model_id": model_id, "filename": filename}
                          })

        response = r.json()

        return jsonify(response), response["status"]

    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]


@views_blueprint.route("/test/config/<model_id>", methods=["GET"])
@cross_origin()
@token_required
def get_available_config(current_user, model_id):
    try:
        r = requests.get(f"http://ai-master:5000/test/config/{model_id}")

        response = r.json()

        return jsonify(response), response["status"]
    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]


@views_blueprint.route("/model/<model_id>/data", methods=["GET"])
@cross_origin()
@token_required
def get_available_data_for_model(current_user, model_id):
    try:
        r = requests.get(f"http://data-provider:5000/model/{model_id}/data")

        response = r.json()

        return jsonify(response), response["status"]
    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]


@views_blueprint.route("/model/<model_id>/test", methods=["POST"])
@cross_origin()
@token_required
def run_model_test(current_user, model_id):
    try:
        user_id = current_user["data"]["id"]
        device = request.json["data"]["device"]

        logging.error(user_id)
        r = requests.post(f"http://ai-master:5000/test/{model_id}", json={"data": {"user_id": user_id, "device": device}}).json()

        logging.error(r)

        return jsonify(r), r["status"]
    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]


@views_blueprint.route("/graph/<model_id>", methods=["GET"])
@cross_origin()
@token_required
def get_test_graph_data_for_model(current_user, model_id):

    try:
        r = requests.get(f"http://model-info:5000/graph/{model_id}").json()

        logging.error(r)

        return jsonify(r), r["status"]
    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]

@views_blueprint.route("/devices", methods=["GET"])
@cross_origin()
@token_required
def get_device_information(current_user):
    # Send request to AI Master
    try:
        user_id = current_user["data"]["id"]
        logging.error(user_id)
        r = requests.get(f"http://ai-master:5000/devices").json()

        logging.error(r)

        return jsonify(r), r["status"]
    except requests.exceptions.ConnectionError as e:
        response = {
            "status": 500,
            "message": f"Connection error. {e}"
        }

        return jsonify(response), response["status"]
