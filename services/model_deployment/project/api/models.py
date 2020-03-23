from sqlalchemy.sql import func
from project import database
import os


class ModelDefinition(database.Model):

    __tablename__ = "models"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    model_title = database.Column(database.String(256), nullable=False)
    path_to_model = database.Column(database.String(512))  # Contains the path to uploaded model config file
    deployed_by = database.Column(database.Integer, nullable=False)
    model_framework = database.Column(database.String(128), nullable=False)

    def __init__(self, model_title, path_to_model, deployed_by, model_framework):
        self.model_title = model_title
        self.path_to_model = path_to_model
        self.deployed_by = deployed_by
        self.model_framework = model_framework

    def to_json(self):
        return {
            "id": self.id,
            "model_title": self.model_title,
            "path": os.path.basename(self.path_to_model),
            "deployed_by": self.deployed_by,
            "model_framework": self.model_framework
        }
