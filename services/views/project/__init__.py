import os
from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="views")

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    from project.api.views import views_blueprint
    app.register_blueprint(views_blueprint)

    return app


