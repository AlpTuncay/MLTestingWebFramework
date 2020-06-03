from flask import Blueprint, jsonify, request, current_app
from flask_mail import Message
from project import mail
from datetime import datetime
import logging
import requests


mailer_blueprint = Blueprint("mailer", __name__)


@mailer_blueprint.route("/send", methods=["POST"])
def send_mail():
        model_id = request.json["data"]["model_id"]
        test_score = request.json["data"]["test_acc"]
        test_loss = request.json["data"]["test_loss"]
        last_test_time = request.json["data"]["last_test_time"]
        test_duration = request.json["data"]["test_duration"]
        test_status = request.json["data"]["test_status"]
        reason = request.json["data"]["reason"]
        requester_id = request.json["data"]["requester_id"]

        last_test_time = datetime.fromtimestamp(last_test_time)

        # Currently no information of test requester. User id needs to be added to test request object.
        # Here send a request to register service and get user information using user_id.

        requester = requests.get(f"http://register:5000/users/{requester_id}").json()["data"]
        model = requests.get(f"http://models:5000/models/{model_id}").json()["data"]

        logging.error(requester)
        logging.error(model)

        requester_mail = requester["email"]

        if test_status == "Success":
            message = f"Dear {requester['username']},\
                    \nYour test has been run successfully.\
                    \nDetails:\
                    \nScore: {test_score}\nLoss: {test_loss}\nDuration: {test_duration}\nTime of test: {last_test_time}"
        else:
            message = f"Dear {requester['username']},\
                    \nSome issues have occurred during testing.\
                    \nDetails:\
                    \nStatus: {test_status}\nTime of test: {last_test_time}\nReason: {reason}"

        msg = Message(f"Model Test Result for {model['model_title']}", sender=current_app.config["MAIL_USERNAME"], recipients=[requester_mail])
        msg.body = message
        mail.send(msg)

        return "Sent"
