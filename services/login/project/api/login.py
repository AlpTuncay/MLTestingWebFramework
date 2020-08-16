from flask import Blueprint, jsonify, request
from project import database
from werkzeug.security import check_password_hash
from project.api.models import User
from flask import current_app
import jwt

login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/validate", methods=["POST"])
def validate():
    auth_token = request.json["auth_token"]

    try:
        payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"))

        response = {
            "status": 200,
            "message": "Valid"
        }

        return jsonify(response), response["status"]
    except jwt.ExpiredSignatureError:

        response = {
            "status": 400,
            "message": "Signature Expired"
        }

        return jsonify(response), response["status"]
    except jwt.InvalidSignatureError:

        response = {
            "status": 400,
            "message": "Invalid Expired"
        }

        return jsonify(response), response["status"]

@login_blueprint.route("/login", methods=["POST"])
def login():
    # User sends a post request, with credentials
    email = request.json["data"]["email"]
    password = request.json["data"]["password"]

    response = {
        "status": 400,
        "message": "Invalid payload."
    }

    if not email or not password:
        return jsonify(response), 400

    try:
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response["status"] = 200
                response["message"] = "Successfully logged in"
                response["token"] = auth_token.decode()

                return jsonify(response), 200
            else:
                return jsonify(response), 400
        else:
            response["status"] = 404
            response["message"] = "Check email/password"

            return jsonify(response), 404
    except Exception as e:
        response["status"] = 500
        response["message"] = f"Error while logging in. {e}"

        return jsonify(response), 500
