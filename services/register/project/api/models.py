from sqlalchemy.sql import func
from project import database
from werkzeug.security import generate_password_hash


class User(database.Model):

    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String(256), nullable=False)
    email = database.Column(database.String(256), nullable=False, unique=True)
    name = database.Column(database.String(256), nullable=False)
    surname = database.Column(database.String(256), nullable=False)
    password = database.Column(database.String(512), nullable=False)
    created_at = database.Column(database.DateTime, default=func.now())

    def __init__(self, username, email, name, surname, password):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname
        self.password = generate_password_hash(password)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "created_at": self.created_at
        }
