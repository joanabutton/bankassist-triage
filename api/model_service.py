from pathlib import Path
import joblib
import os
from api.mock_model import MockModel

#MODEL_PATH = Path("models/champion_model.pkl")


class ModelService:

    def __init__(self):

        use_mock = os.getenv(
            "USE_MOCK_MODEL",
            "true"
        ).lower() == "true"

        if use_mock:
            self.model = MockModel()
        else:
            self.model = joblib.load(
                "models/champion_model.pkl"
            )

    def is_loaded(self):
        return self.model is not None

    def predict(self, message):

        prediction = self.model.predict([message])[0]

        confidence = 0.0

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba([message])[0]
            confidence = float(max(probabilities))

        return {
            "intent": str(prediction),
            "confidence": confidence
        }
