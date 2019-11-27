import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    database.init_app(app)

    from project.api.login import login_blueprint
    app.register_blueprint(login_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': database}

    return app