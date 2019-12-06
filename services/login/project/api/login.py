from flask import Blueprint, jsonify
from project import database
import json


login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login", methods=["POST"])
def login():
    # User sends a post request, with credentials
    # A token with a TTL, which will be added to each request user is sending, is returned to the user
    # A database entry will be created with the user id and token so that other services can verify the user is indeed
    # logged in
    pass


@login_blueprint.route("/logout", methods=["POST"])
def logout():
    # User's database entry will be destroyed
    pass


@login_blueprint.route("/verify/<token>/<user_id>", methods=["GET"])
def verify_token(token, user_id):
    pass
