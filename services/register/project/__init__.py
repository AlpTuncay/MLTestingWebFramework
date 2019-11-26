import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.messaging.Producer import Producer

database = SQLAlchemy()

producer = Producer("rabbitmq-broker")

def create_app():

    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    database.init_app(app)

    from project.api.register import user_blueprint
    app.register_blueprint(user_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': database}

    return app