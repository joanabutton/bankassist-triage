import os
import mlflow
import mlflow.sklearn


MODEL_URI = "models:/BankAssist-Intent-Classifier@champion"


class ModelService:

    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        mlflow.set_tracking_uri(
            os.getenv(
                "MLFLOW_TRACKING_URI",
                "http://localhost:5001"
            )
        )

        self.model = mlflow.sklearn.load_model(MODEL_URI)

    def is_loaded(self):
        return self.model is not None

    def predict(self, message: str):

        prediction = self.model.predict([message])[0]

        confidence = 0.0

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba([message])[0]
            confidence = float(max(probabilities))

        return {
            "intent": str(prediction),
            "confidence": confidence
        }
