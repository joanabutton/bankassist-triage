from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.model_service import ModelService
from api.schemas import PredictionRequest, PredictionResponse


app = FastAPI(
    title="BankAssist Triage API",
    description="ML-powered bank customer query intent classification and routing API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_service = ModelService()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model_service.is_loaded(),
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        result = model_service.predict(request.message)

        intent = result["intent"]
        confidence = result["confidence"]

        return {
            "intent": intent,
            "confidence": confidence,
            "route": get_route(intent),
            "requires_human_review": requires_human_review(confidence),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}",
        )
