from fastapi import APIRouter, HTTPException
from schemas.request import ProductIngestRequest
from services.aggregator import vpms

router = APIRouter()

@router.post("/analyze-product")
async def analyze_product_endpoint(request: ProductIngestRequest):
    try:
        return await vpms(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
