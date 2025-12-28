from pydantic import BaseModel, Field
from typing import List, Optional


# ---------------------------
# Core measurement schema
# ---------------------------

class Measurement(BaseModel):
    """
    Represents a single aggregated visual measurement
    for a product dimension.
    """

    score: float = Field(
        ...,
        ge=-5.0,
        le=5.0,
        description="Visual score in range [-5.0, +5.0]"
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence level for the score in range [0.0, 1.0]"
    )


# ---------------------------
# Visual measurement bundle
# ---------------------------

class VisualMeasurements(BaseModel):
    """
    Aggregated visual measurements for a product.
    """

    gender_expression: Measurement
    visual_weight: Measurement
    embellishment: Measurement
    unconventionality: Measurement
    formality: Measurement


# ---------------------------
# Optional visual attributes
# ---------------------------

class VisualAttributes(BaseModel):
    """
    Additional observable visual attributes inferred
    from the product images.
    """

    dominant_colors: Optional[List[str]] = None
    transparency: Optional[str] = None
    textures: Optional[List[str]] = None
    wirecore_visible: Optional[bool] = None


# ---------------------------
# Final API response schema
# ---------------------------

class AnalyzeProductResponse(BaseModel):
    """
    Final response returned by the Visual Product Measurement System.
    This is the only public output contract of the API.
    """

    product_id: int
    visual_measurements: VisualMeasurements
    visual_attributes: Optional[VisualAttributes] = None
    ambiguities: List[str] = []
