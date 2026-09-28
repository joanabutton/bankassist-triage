#Request/response Schemas

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Customer banking query"
    )


class PredictionResponse(BaseModel):
    message: str
    intent: str
    confidence: float
    destination: str
    
    
 
 
