from fastapi import APIRouter, HTTPException
from schemas.request import ProductIngestRequest
from services.aggregator import orchestrator
import json

router = APIRouter()

@router.post("/analyze-product")
async def analyze_product_endpoint(request: ProductIngestRequest):
    try:
        return await orchestrator(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# result = await analyze_product_endpoint({
#     "product_id": 235396,
#     "category": "Sunglasses",
#     "declared_image_count": 6,
    # "image_urls": [
    #   "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2781_18_08_2025.jpg",
    #   "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2780_18_08_2025.jpg",
    #   "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2783_18_08_2025.jpg",
    #   "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2784_18_08_2025.jpg",
    #   "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2786_18_08_2025.jpg",
    #   "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2781_image_pla_18_08_2025.jpg"
    # ]
#   })

# import asyncio
# import json

# # whatever imports you already have

# async def main():
#     payload = ProductIngestRequest(
#         product_id=235396,
#         category="Sunglasses",
#         declared_image_count=6,
#         image_urls=[
#         "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2781_18_08_2025.jpg",
#         "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2780_18_08_2025.jpg",
#         "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2783_18_08_2025.jpg",
#         "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2784_18_08_2025.jpg",
#         "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2786_18_08_2025.jpg",
#         "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2781_image_pla_18_08_2025.jpg"
#         ]
#     )

#     result = await analyze_product_endpoint(payload)  # ✅ await it
#     print(type(result))
#     print(json.dumps(result, indent=2))

# if __name__ == "__main__":
#     asyncio.run(main())
