from flask import Blueprint, jsonify, request
from project import database
from sqlalchemy import exc
from project.api.models import User
from project import producer
import json

user_blueprint = Blueprint("users", __name__)


'''
In each endpoint, the response returned would be sent to the RabbitMQ queue for the request sender.
'''

@user_blueprint.route("/users", methods=["POST"])
def register_user():
    username = request.json["data"]["username"]
    email = request.json["data"]["email"]
    name = request.json["data"]["name"]
    surname = request.json["data"]["surname"]
    password = request.json["data"]["password"]

    user = User(username=username, name=name, surname=surname, email=email, password=password)

    try:
        user_check = User.query.filter_by(email=email).first() # First check if the user exists
        if not user_check:
            database.session.add(user)
            database.session.commit()

            status = {
                "status": 201,
                "message": "User registered successfully."
            }

            return jsonify(status)
        else:
            status = {
                "status": 400,
                "message": "User already exists."
            }

            return jsonify(status)
    except exc.IntegrityError:
        database.session.rollback()

        status = {
            "status": 500,
            "message": "Error ocurred while registering"
        }

        return jsonify(status)


@user_blueprint.route("/users/all", methods=["GET"])
def get_all_users():
    users = User.query.all()

    if not users:
        status = {
            "status": 404,
            "message": "Cannot fetch users."
        }

        return jsonify(status)
    else:
        return jsonify({
            "status": 200,
            "message": "Successfully fetched users",
            "data": [user.to_json() for user in users]
        })


@user_blueprint.route("/users/<user_id>", methods=["GET"])
def get_one_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({
            "status": 404,
            "message": "Cannot find user."
        })
    else:
        return jsonify({
            "status": 200,
            "message": "Fetched user successfully.",
            "data": user.to_json()
        })


@user_blueprint.route("/users/update/<user_id>", methods=["POST"])
def update_user(user_id):
    username = request.json["data"]["username"]
    email = request.json["data"]["email"]
    name = request.json["data"]["name"]
    surname = request.json["data"]["surname"]

    user = User.query.filter_by(id=user_id).first()

    if user:
        user.username = username
        user.name = name
        user.surname = surname

        user_check = User.query.filter_by(email=email).first()

        if user_check and user.email != email:
            return jsonify({
                "status": 400,
                "message": "User with the email exists."
            })
        else:
            user.email = email
            try:
                database.session.commit()
                return jsonify({
                    "status": 200,
                    "message": "Updated user successfully."
                })
            except exc.IntegrityError:
                return jsonify({
                    "status": 500,
                    "message": "Error while updating user."
                })


@user_blueprint.route("/users/delete/<user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user:
        try:
            database.session.delete(user)
            database.session.commit()

            return jsonify( {
                "status": 200,
                "message": "Deleted user successfully"
            })
        except exc.IntegrityError:
            database.session.rollback()

            return jsonify({
                "status": 400,
                "message": "Error"
            })
    else:

        return jsonify({
            "status": 404,
            "message": "User cannot be found"
        })
