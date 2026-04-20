from fastapi import APIRouter, HTTPException
from app.schemas.prediction_schema import PredictionRequest, PredictionResponse
from app.services.prediction_service import prediction_service

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty")
    
    result = prediction_service.predict(request.resume_text)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result
