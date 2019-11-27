from sqlalchemy.sql import func
from project import database
from flask_login import UserMixin


class Login(database.Model):
    __tablename__ = "logged_in"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    user_id = database.Column(database.Integer, nullable=False)
    auth_token = database.Column(database.String(512), nullable=False)

    def __init__(self, user_id, auth_token):
        self.user_id = user_id
        self.auth_token = auth_token

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "auth_token": self.auth_token
        }


class User(UserMixin, database.Model):

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
