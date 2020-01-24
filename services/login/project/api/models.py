from sqlalchemy.sql import func
from project import database
from flask import current_app
import datetime
import jwt


class User(database.Model):

        __tablename__ = "users"

        id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        username = database.Column(database.String(256), nullable=False)
        email = database.Column(database.String(256), nullable=False, unique=True)
        name = database.Column(database.String(256), nullable=False)
        surname = database.Column(database.String(256), nullable=False)
        password = database.Column(database.String(512), nullable=False)
        created_at = database.Column(database.DateTime, default=func.now())

        def __init__(self, username, email, name, surname):
            self.username = username
            self.email = email
            self.name = name
            self.surname = surname

        def to_json(self):
            return {
                "id": self.id,
                "username": self.username,
                "email": self.email,
                "name": self.name,
                "surname": self.surname,
                "created_at": self.created_at
            }

        def encode_auth_token(self, user_id):
            try:
                current_app.logger.debug(f"TOKEN_EXP_DAYS: {current_app.config.get('TOKEN_EXP_DAYS')}")
                payload = {
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config.get("TOKEN_EXP_DAYS")),
                    "iat": datetime.datetime.utcnow(),
                    "sub": user_id
                }
                token = jwt.encode(payload, current_app.config.get("SECRET_KEY"))

                current_app.logger.debug(f"TOKEN: {token}")

                return token

            except Exception as e:
                current_app.logger.error(e)
                return e

        def decode_auth_token(self, token):
            try:
                payload = jwt.decode(token, current_app.config.get("SECRET"))
                return payload["sub"]
            except jwt.ExpiredSignatureError:
                return "Signature expired."
            except jwt.InvalidSignatureError:
                return "Invalid token."
