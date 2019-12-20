import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    app.logger.debug("Initiating app")

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    app.logger.debug("Initiating database")
    database.init_app(app)

    app.logger.debug("Registering blueprint")
    from project.api.login import login_blueprint
    app.register_blueprint(login_blueprint)

    app.logger.debug("Blueprint registered")

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': database}

    return app