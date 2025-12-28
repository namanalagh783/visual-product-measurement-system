from services.image_validation import validate_product_images
from services.vision_analysis import analyze_product
from services.aggregation import aggregate_scores


class PipelineError(Exception):
    pass


async def vpms(payload) -> dict:
    """
    Visual Product Measurement System pipeline

    Stage 1: Image validation
    Stage 2: Vision analysis
    Stage 3: Aggregation
    """

    # -------- Stage 1 --------
    stage1 = await validate_product_images(payload)

    if not stage1.get("success"):
        raise PipelineError(
            stage1["payload"].get("error", "Image validation failed")
        )

    validated_payload = stage1["payload"]

    # -------- Stage 2 --------
    stage2 = analyze_product(validated_payload)

    if "error" in stage2:
        raise PipelineError(stage2["error"])

    # -------- Stage 3 --------
    final_output = aggregate_scores(stage2)

    return final_output


