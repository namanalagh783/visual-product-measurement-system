import requests
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API key error")
# from PIL import Image

# Initialize the NEW client (v1 API)
client = genai.Client(api_key=API_KEY)

# --- 2. DEFINE OUTPUT SCHEMA (Using Pydantic) ---
# The new SDK loves Pydantic. It's much cleaner than TypedDict.

class Measurement(BaseModel):
    score: float
    confidence: float
    reasoning: str

class VisualMeasurements(BaseModel):
    gender_expression: Measurement
    visual_weight: Measurement
    embellishment: Measurement
    unconventionality: Measurement
    formality: Measurement

class VisualAttributes(BaseModel):
    dominant_colors: list[str]
    transparency: str
    textures: list[str]
    wirecore_visible: bool | None = Field(description="Null if temple arm wirecore is not visible")

class ProductAnalysisOutput(BaseModel):
    product_id: str
    visual_measurements: VisualMeasurements
    visual_attributes: VisualAttributes
    ambiguities: list[str]

# --- 3. HELPER FUNCTIONS ---

def download_image_bytes(url: str):
    """Downloads image and returns raw bytes + mime type."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # We need bytes for the new SDK, not just a PIL object
        return response.content, response.headers.get('Content-Type', 'image/jpeg')
    except Exception as e:
        print(f"  [!] Error downloading {url}: {e}")
        return None, None

def analyze_product(payload: dict):
    product_id = str(payload.get("product_id"))
    category = payload.get("category", "Item")
    urls = payload.get("valid_images", [])
    
    print(f"--- Processing {category} (ID: {product_id}) ---")

    # A. Prepare Content List
    # The new SDK accepts a list containing text and "Part" objects for images
    prompt_text = f"""
    Analyze these images of a {category} (ID: {product_id}).
    
    Examine the visual details for:
    1. Gender expression (Masculine/Feminine cues)
    2. Visual weight (Thick/Heavy vs Thin/Light)
    3. Embellishments (Decorations, studs, crystals)
    4. Unconventionality (How unique or weird it is)
    5. Formality (Casual vs Formal)
    
    Also identify dominant colors, textures, and transparency.
    """
    
    contents = [prompt_text]

    # B. Download and Append Images
    print(f"  Downloading {len(urls)} images...")
    valid_count = 0
    
    for url in urls:
        img_bytes, mime_type = download_image_bytes(url)
        if img_bytes:
            # New SDK Syntax: Create a 'Part' from bytes
            image_part = types.Part.from_bytes(data=img_bytes, mime_type=mime_type)
            contents.append(image_part)
            valid_count += 1
            
    if valid_count == 0:
        return {"error": "No valid images available."}

    # C. Call Gemini (New Syntax)
    print("  Sending data to Gemini...")
    
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=ProductAnalysisOutput 
            )
        )
        
        # With the new SDK, response.parsed is automatically a Python object!
        # We convert it back to dict for generic usage/printing
        return response.parsed.model_dump()
        
    except Exception as e:
        return {"error": f"API Error: {e}"}

# --- 4. EXECUTION ---
# Your Payload
test_payload = {
    "product_id": 235396,
    "category": "Sunglasses",
    "declared_image_count": 6,
    "received_image_count": 6,
    "valid_images": [
        "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2781_18_08_2025.jpg",
        "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2780_18_08_2025.jpg",
        "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2783_18_08_2025.jpg",
        "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2784_18_08_2025.jpg",
        "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2786_18_08_2025.jpg",
        "https://static5.lenskart.com/media/catalog/product/pro/1/thumbnail/1325x636/9df78eab33525d08d6e5fb8d27136e95//l/i/brown-black-full-rim-cat-eye-lenskart-sg-nuun-lk-s18217af-sunglasses__dsc2781_image_pla_18_08_2025.jpg"
    ],
    "invalid_images": [],
    "status": "images_validated",
    "notes": [
        "Declared image count matches received URLs"
    ],
    "message": "At least one image is available for vision analysis"
}

if __name__ == "__main__":
    result = analyze_product(test_payload)
    import json
    print("\n--- FINAL OUTPUT ---")
    print(json.dumps(result, indent=2))