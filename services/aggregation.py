def aggregate_scores(stage2_output: dict) -> dict:
    """
    Stage-3: Aggregation & normalization

    Takes raw AI output and produces final
    product-level visual measurements.
    """

    final_measurements = {}

    for key, value in stage2_output["visual_measurements"].items():
        score = max(-5.0, min(5.0, value["score"]))
        confidence = max(0.0, min(1.0, value["confidence"]))

        final_measurements[key] = {
            "score": round(score, 2),
            "confidence": round(confidence, 2)
        }

    return {
        "product_id": stage2_output["product_id"],
        "visual_measurements": final_measurements,
        "visual_attributes": stage2_output.get("visual_attributes", {}),
        "ambiguities": stage2_output.get("ambiguities", [])
    }
