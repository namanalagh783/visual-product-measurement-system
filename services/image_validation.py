import asyncio
import httpx
from schemas.request import ProductIngestRequest

# --- 1. THE HELPER FUNCTION (Checks one image) ---
async def check_single_url(client, url):
    try:
        # Check headers without downloading the full image
        response = await client.get(url, follow_redirects=True, timeout=5.0)
        
        # Rule 1: Status Code 200-299
        if response.status_code < 200 or response.status_code >= 300:
            return str(url), False, f"HTTP Status {response.status_code}"

        # Rule 2: Content-Type must be image
        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            return str(url), False, f"Invalid Content-Type: {content_type}"

        return str(url), True, "OK"

    except httpx.TimeoutException:
        return str(url), False, "Timeout"
    except Exception as e:
        return str(url), False, "Unreachable / Connection Error"

# --- 2. THE MAIN FUNCTION (Call this!) ---
async def validate_product_images(product_data):
    """
    Takes a dictionary with product details.
    Returns a dictionary with validation results.
    """
    
    # Extract data (Safe conversion of product_id to string)
    p_id = str(product_data.product_id)
    category = product_data.category
    declared_count = product_data.declared_image_count or 0
    urls = product_data.image_urls or []
    
    # Prepare lists
    valid_images = []
    invalid_images = []

    # Run checks in parallel
    async with httpx.AsyncClient() as client:
        tasks = [check_single_url(client, str(url)) for url in urls]
        results = await asyncio.gather(*tasks)

    # Sort results
    for url, is_valid, reason in results:
        if is_valid:
            valid_images.append(url)
        else:
            invalid_images.append({"url": url, "reason": reason})

    # --- FAILURE LOGIC ---
    if not valid_images:
        return {
            "error": "No valid images could be retrieved",
            "product_id": p_id,
            "invalid_images": invalid_images
        }

    return {
        "product_id": p_id,
        "category": category,
        "declared_image_count": declared_count,
        "received_image_count": len(urls),
        "valid_images": valid_images,
        "invalid_images": invalid_images,
        "status": "images_validated",
        "message": "At least one image is available for vision analysis"
    }

# --- 3. HOW TO TEST IT ---
# if __name__ == "__main__":
    
#     # A. Define your test data (Simulating the CSV row)
#     test_input = ProductIngestRequest(
#         product_id=235396,
#         category="Sunglasses",
#         declared_image_count=6,
#         image_urls=[
#             "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2781_18_08_2025.jpg",
#             "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2780_18_08_2025.jpg",
#             "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2783_18_08_2025.jpg",
#             "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2784_18_08_2025.jpg",
#             "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2786_18_08_2025.jpg",
#             "https://static5.lekart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2781_image_pla_18_08_2025.jpg",
#         ],
#     )

#     # B. Run the function
#     # (Since it uses async, we need asyncio.run to start it)
#     result = asyncio.run(validate_product_images(test_input))

#     # C. Print Result
#     import json
#     print(json.dumps(result, indent=2))