import os
from flask import Flask, current_app
from flask_mail import Mail


mail = Mail()


def create_app():

    app = Flask(__name__)
    app.logger.debug("Initiating app")

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    mail.init_app(app)

    app.logger.debug("Registering blueprint")
    from project.api.mailer import mailer_blueprint
    app.register_blueprint(mailer_blueprint)

    app.logger.debug("Blueprint registered")

    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app
