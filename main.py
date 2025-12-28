from fastapi import FastAPI
from api.analyse_product import router

app = FastAPI(
    title="Visual Product Measurement System - Stage 1",
    description="Image Ingestion and Validation API",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "VPMS Stage-1 is running"}