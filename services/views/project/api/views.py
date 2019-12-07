from flask import Blueprint, render_template


views_blueprint = Blueprint("views", __name__, template_folder="./templates")


@views_blueprint.route("/register", methods=["GET"])
def register():
    return render_template("/register/register.html")
