#Request/response Schemas

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=3,
        max_length=2000
    )


class PredictionResponse(BaseModel):
    intent: str
    confidence: float
    route: str
    requires_human_review: bool
    
    
 
 
