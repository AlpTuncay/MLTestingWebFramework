from sqlalchemy.sql import func
from project import database
import os


class ProviderObject(database.Model):

    __tablename__ = "data_store"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    model_id = database.Column(database.Integer, nullable=False)
    data_path = database.Column(database.String(512), nullable=False)

    def __init__(self, model_id, data_path):
        self.model_id = model_id
        self.data_path = data_path

    def to_json(self):
        return {
            "id": self.id,
            "model_id": self.model_id,
            "data_path": self.data_path,
            "filename": os.path.basename(self.data_path)
        }
