from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import PredictionRequest, PredictionResponse
from api.model_service import ModelService
from api.routing import get_destination

app = FastAPI(
    title="BankAssist Triage API",
    version="1.0.0",
    description="API for classifying and routing banking customer queries."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict this after frontend deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_service = ModelService()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model_service.is_loaded()
    }


@app.get("/")
def root():
    return {
        "service": "BankAssist Triage API",
        "status": "running"
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    try:
        prediction = model_service.predict(request.message)

        destination = get_destination(prediction["intent"])

        return {
            "message": request.message,
            "intent": prediction["intent"],
            "confidence": prediction["confidence"],
            "destination": destination
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
