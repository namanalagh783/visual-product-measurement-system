
from image_validation import validate_product_images
from vision_analysis import analyze_product
from aggregation import aggregate_scores
import asyncio
import json


def orchestrator(test_input : dict) -> dict:
    result = asyncio.run(validate_product_images(test_input))
    # print(json.dumps(result, indent=2))
    result2 = analyze_product(result)
    # print(json.dumps(result2))
    result3 = aggregate_scores(result2)
    return result3



test_input1 = {
        "product_id": 231031,  # Note: It handles Int or String now
        "category": "Eyeglasses",
        "declared_image_count": 2,
        "image_urls": [
            "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
            "https://this-does-not-exist.com/fail.jpg"
        ]
    }

    # B. Run the function
    # (Since it uses async, we need asyncio.run to start it)
# result = asyncio.run(validate_product_images(test_input))
# # print(json.dumps(result, indent=2))
# result2 = analyze_product(result)
# # print(json.dumps(result2))
# result3 = aggregate_scores(result2)
# print(json.dumps(result3, indent=2))
result = orchestrator(test_input1)
print(json.dumps(result, indent=2))