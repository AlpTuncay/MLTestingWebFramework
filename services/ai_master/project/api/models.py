from sqlalchemy.sql import func
from project import database


class ModelState(database.Model):

    __tablename__ = "model_state"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    model_id = database.Column(database.Integer, nullable=False)
    test_accuracy = database.Column(database.Float, nullable=False)
    test_loss = database.Column(database.Float, nullable=False)
    last_test_time = database.Column(database.DateTime, nullable=False)
    test_duration = database.Column(database.DateTime, nullable=False)

    def __init__(self, model_id, test_accuracy, test_loss, last_test_time, test_duration):
        self.model_id = model_id
        self.test_accuracy = test_accuracy
        self.test_loss = test_loss
        self.last_test_time = last_test_time
        self.test_duration = test_duration

    def to_json(self):
        return {
            "id": self.id,
            "model_id": self.model_id,
            "test_acc": self.test_accuracy,
            "test_loss": self.test_loss,
            "last_test_time": self.last_test_time,
            "test_duration": self.test_duration
        }

# WIP -> Find a way to store test results.
