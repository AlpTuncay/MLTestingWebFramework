from flask import Blueprint, jsonify, request
from project import database
from werkzeug.security import check_password_hash
from project.api.models import User


login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login", methods=["POST"])
def login():
    # User sends a post request, with credentials
    # A token with a TTL, which will be added to each request user is sending, is returned to the user
    # A database entry will be created with the user id and token so that other services can verify the user is indeed
    # logged in
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


@login_blueprint.route("/logout", methods=["POST"])
def logout():
    # User's database entry will be destroyed
    pass
