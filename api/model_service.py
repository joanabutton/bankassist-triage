import os

import mlflow
import mlflow.sklearn
from mlflow import MlflowClient


MODEL_NAME = "BankAssist-Intent-Classifier"
MODEL_ALIAS = "champion"
MODEL_URI = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"


class ModelService:
    def __init__(self):
        self.tracking_uri = os.getenv(
            "MLFLOW_TRACKING_URI",
            "http://localhost:5001",
        )

        mlflow.set_tracking_uri(self.tracking_uri)

        self.client = MlflowClient(
            tracking_uri=self.tracking_uri
        )

        self.model = None
        self.loaded_version = None

        self.load_model()

    def load_model(self):
        model_version = self.client.get_model_version_by_alias(
            MODEL_NAME,
            MODEL_ALIAS,
        )

        if (
            self.model is None
            or self.loaded_version != model_version.version
        ):
            self.model = mlflow.sklearn.load_model(MODEL_URI)

            self.loaded_version = model_version.version

            print(
                f"Loaded {MODEL_NAME} "
                f"@{MODEL_ALIAS} "
                f"(version {self.loaded_version})"
            )

    def is_loaded(self) -> bool:
        return self.model is not None

    def predict(self, message: str) -> dict:
        # Check whether @champion changed
        self.load_model()

        prediction = self.model.predict([message])[0]

        probabilities = self.model.predict_proba([message])[0]
        confidence = float(max(probabilities))

        return {
            "intent": str(prediction),
            "confidence": confidence,
        }
