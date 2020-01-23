from flask import Blueprint, request, current_app, jsonify
import requests
import logging
from functools import wraps
import jwt
from flask_cors import cross_origin

views_blueprint = Blueprint("api", __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            response = {
                "status": 401,
                "message": "Missing token."
            }
            return jsonify(response)

        try:
            token_decoded = jwt.decode(token, current_app.config.get("SECRET_KEY"))
            try:
                current_user = requests.get(f"http://register:5000/users/{token_decoded['sub']}").json()
                return f(current_user, *args, **kwargs)
            except requests.exceptions.ConnectionError:
                response = {
                    "status": 500,
                    "message": "Connection error occurred."
                }

                return jsonify(response)

        except Exception as e:

            response = {
                "status": 401,
                "message": "Invalid token"
            }

            return jsonify(response)

    return decorated


@views_blueprint.route("/register", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
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
@cross_origin(origin="*", headers=["Content-Type"])
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
@token_required
def profile(user):
    return jsonify(user)
