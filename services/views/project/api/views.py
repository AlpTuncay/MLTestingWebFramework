from flask import Blueprint, render_template, request, redirect
import requests
import logging

views_blueprint = Blueprint("views", __name__, template_folder="./templates")



@views_blueprint.route("/register", methods=["GET"])
def render_register_view():
    return render_template("/register/register.html")


@views_blueprint.route("/register", methods=["POST"])
def register_user():
    global response
    username = request.form["username"]
    email = request.form["email"]
    name = request.form["name"]
    surname = request.form["surname"]
    password = request.form["password"]

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
        response = r.json()
        if response["status"] == 201:
            return redirect("/login")
        else:
            return render_template("/error/error.html", error_code=response["status"], error_message=response["message"])
    except requests.exceptions.ConnectionError:
        # print(f"Cannot post to register service")
        logging.error("Cannot post to register service")
        # exit(1)



@views_blueprint.route("/login", methods=["GET"])
def render_login_view():
    return render_template("/login/login.html")
