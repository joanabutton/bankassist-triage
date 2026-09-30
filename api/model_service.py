import os
import joblib
import mlflow
import mlflow.sklearn


MODEL_URI = "models:/BankAssist-Intent-Classifier@champion"


class ModelService:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        model_source = os.getenv("MODEL_SOURCE", "mlflow")

        if model_source == "local":
            self.model = joblib.load(
                "models/champion_model.pkl"
            )
            return

        tracking_uri = os.getenv(
            "MLFLOW_TRACKING_URI",
            "http://localhost:5001"
        )

        mlflow.set_tracking_uri(tracking_uri)

        self.model = mlflow.sklearn.load_model(MODEL_URI)

    def is_loaded(self):
        return self.model is not None

    def predict(self, message: str):
        prediction = self.model.predict([message])[0]

        probabilities = self.model.predict_proba([message])[0]
        confidence = float(max(probabilities))

        return {
            "intent": str(prediction),
            "confidence": confidence,
        }
