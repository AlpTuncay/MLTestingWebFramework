import os
from flask import Flask
from flask_cors import CORS

cors = CORS()

def create_app():
    app = Flask(__name__)

    cors.init_app(app)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    app.config["CORS_HEADERS"] = "Access-Control-Allow-Origin"

    from project.api.api import views_blueprint
    app.register_blueprint(views_blueprint)

    return app


