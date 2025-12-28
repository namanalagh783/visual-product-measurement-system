from pydantic import BaseModel, HttpUrl, Field
from typing import List


class ProductIngestRequest(BaseModel):
    """
    Input schema for the Visual Product Measurement System.

    Represents a single product entry along with
    its associated image URLs.
    """

    product_id: int = Field(
        ...,
        description="Unique identifier for the product"
    )

    category: str = Field(
        ...,
        description="Product category (informational metadata)"
    )

    declared_image_count: int = Field(
        ...,
        ge=0,
        description="Declared number of images for the product"
    )

    image_urls: List[HttpUrl] = Field(
        ...,
        description="List of image URLs associated with the product"
    )
