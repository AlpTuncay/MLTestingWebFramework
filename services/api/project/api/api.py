from flask import Blueprint, request, current_app, jsonify
import requests
import logging
from functools import wraps
import jwt
from flask_cors import cross_origin

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


@views_blueprint.route("/validate", methods=["GET"])
@cross_origin()
@token_required
def validate_token(current_user):
    pass


@views_blueprint.route("/user/profile", methods=["GET"])
@cross_origin()
@token_required
def profile(current_user):
    user_information = current_user["data"]
    user_id = user_information["id"]

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


@views_blueprint.route("/model/deploy", methods=["POST"])
@cross_origin()
@token_required
def deploy_model(user):
    pass
