from sqlalchemy.sql import func
from project import database


class ModelState(database.Model):

    __tablename__ = "model_state"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    model_id = database.Column(database.Integer, nullable=False)
    test_accuracy = database.Column(database.Float, nullable=False)
    test_loss = database.Column(database.Float, nullable=False)
    last_test_time = database.Column(database.DateTime, nullable=False)
    test_duration = database.Column(database.Float, nullable=False)
    test_status = database.Column(database.String, nullable=False)
    test_device = database.Column(database.String, nullable=False)

    def __init__(self, model_id, test_accuracy, test_loss, last_test_time, test_duration, test_status, test_device):
        self.model_id = model_id
        self.test_accuracy = test_accuracy
        self.test_loss = test_loss
        self.last_test_time = last_test_time
        self.test_duration = test_duration
        self.test_status = test_status
        self.test_device = test_device

    def to_json(self):
        return {
            "id": self.id,
            "model_id": self.model_id,
            "test_acc": round(self.test_accuracy, 2),
            "test_loss": round(self.test_loss, 2),
            "last_test_time": self.last_test_time.strftime("%d/%m/%Y %H:%M"),
            "test_duration": round(self.test_duration, 2),
            "test_status": self.test_status,
            "test_device": self.test_device
        }
