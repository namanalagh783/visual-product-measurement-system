# AI-Powered Visual Product Measurement System

## 🚀 Overview

This project is a prototype for an automated **Visual Product Measurement System**. The goal was to solve a common problem in e-commerce: product catalogs rely heavily on manual tagging, which is slow, subjective, and inconsistent.

Instead of asking a human to tag a pair of glasses as "retro" or "formal," this system uses a vision-enabled AI model to analyze product images and extract **objective, floating-point scores** across multiple visual dimensions.

I designed the backend as a clean, staged pipeline. The focus wasn't just on "getting it to work," but on engineering a robust system that handles real-world messiness—like broken links or ambiguous images—without crashing.

**Core Engineering Goals:**
* **Separation of Concerns:** Each part of the pipeline does one thing and does it well.
* **Auditable AI:** The AI doesn't just guess; it follows a strict numeric rubric.
* **Structured Output:** The system returns clean JSON that any frontend or database can consume immediately.

---

## 🧠 Design Philosophy

I stuck to a few key principles to keep the scope manageable and the logic sound:

* **Visuals Only:** The system ignores marketing fluff. It looks strictly at what is visible in the pixels (e.g., "thick rim" vs. "classic style").
* **Product-Level Aggregation:** Users upload multiple images (front, side, detail), but the API returns a single, unified score for the product.
* **Fail Gracefully:** If one image link is broken, the request shouldn't fail. The system just notes the error and proceeds with the remaining valid images, adjusting the confidence score accordingly.
* **Stateless Architecture:** The pipeline processes requests on the fly. I omitted a database for this prototype to focus purely on the logic and API design.

---

## 🏗️ High-Level Architecture

I implemented the system as a three-stage pipeline exposed via a single API endpoint. This ensures that the messy work of image downloading and AI inference is completely hidden from the client.

```mermaid
graph TD
    Client[Client Request] --> Stage1
    Stage1[Stage 1: Ingestion & Validation] --> Stage2
    Stage2[Stage 2: Vision Analysis (AI)] --> Stage3
    Stage3[Stage 3: Aggregation & Scoring] --> Final[Final JSON Response]
    
    style Stage1 fill:#e1f5fe,stroke:#01579b
    style Stage2 fill:#fff3e0,stroke:#ff6f00
    style Stage3 fill:#e8f5e9,stroke:#2e7d32
```

*Note: Intermediate results are passed internally between stages but are never exposed to the client to maintain a clean API contract.*

---

## 📥 Input Format

The system processes one product at a time to keep latency predictable.

**Example Payload:**

```json
{
  "product_id": "231031",
  "category": "Eyeglasses",
  "declared_image_count": 5,
  "image_urls": [
    "[https://example.com/image1.jpg](https://example.com/image1.jpg)",
    "[https://example.com/image2.jpg](https://example.com/image2.jpg)"
  ]
}
```

* **`declared_image_count`**: Used for validation (e.g., did we actually receive as many links as the dataset promised?).
* **`category`**: Metadata only; the AI analyzes appearance regardless of category labels.

---

## ⚙️ The Pipeline Stages

### Stage 1: Image Ingestion & Validation
**Responsibility:** *Don't waste compute resources on bad data.*

Before touching the expensive AI model, this stage verifies that the image URLs are reachable and actually contain image data.
* Checks HTTP status codes (200 OK).
* Validates Content-Type headers.
* **Logic:** If *zero* images are valid, the pipeline aborts immediately. If at least one works, we proceed.

### Stage 2: Vision Analysis (AI)
**Responsibility:** *Extract raw visual signals.*

This is where the vision model (e.g., GPT-4o / Gemini) comes in. I use a carefully structured system prompt to force the AI to act as an objective analyst. It evaluates the images on strict **-5.0 to +5.0** scales:

1.  **Gender Expression:** Masculine (-5) ↔ Feminine (+5)
2.  **Visual Weight:** Sleek/Light (-5) ↔ Bold/Heavy (+5)
3.  **Embellishment:** Simple (-5) ↔ Ornate (+5)
4.  **Unconventionality:** Classic (-5) ↔ Avant-garde (+5)
5.  **Formality:** Casual (-5) ↔ Formal (+5)

*It also extracts boolean attributes like "visible wirecore" or "transparency" if clearly seen.*

### Stage 3: Aggregation & Scoring
**Responsibility:** *Turn raw data into a reliable score.*

The raw AI output is smoothed out here.
* **Confidence Calculation:** This isn't just a random number. I derive it based on:
    * How many images were successfully analyzed?
    * Did the AI express uncertainty?
    * Were there conflicting visual signals?
* **Ambiguity Handling:** If the AI says "I can't see the temple clearly," we don't return an error. We return a `null` for that specific attribute and lower the confidence score.

---

## 📤 Final Output (API Response)

This is the only thing the client sees. It's designed to be machine-readable first.

```json
{
  "product_id": "231031",
  "visual_measurements": {
    "gender_expression": {
      "score": 0.35,
      "confidence": 0.9
    },
    "visual_weight": {
      "score": 0.25,
      "confidence": 0.95
    }
  },
  "visual_attributes": {
    "dominant_colors": ["Black", "Silver"],
    "transparency": "Opaque",
    "textures": ["Matte", "Smooth"],
    "wirecore_visible": null
  },
  "ambiguities": []
}
```

---

## 📂 Code Structure

I organized the codebase to make it easy to test each part in isolation.

```bash
backend/
├── main.py                # App entry point (FastAPI)
├── api/
│   └── analyze_product.py # The endpoint logic
├── services/
│   ├── image_validation.py # Stage 1 logic
│   ├── vision_analysis.py  # Stage 2 logic (AI interaction)
│   ├── aggregation.py      # Stage 3 logic
│   └── aggregator.py       # Orchestrator (ties stages together)
├── schemas/               # Pydantic models (Type safety!)
│   ├── request.py
│   └── response.py
└── exceptions/            # Custom error handling
```

---

## 🛠️ How to Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the server:**
    ```bash
    uvicorn app.main:app --reload
    ```

3.  **Test it:**
    Send a `POST` request to `http://localhost:8000/analyze-product` with the JSON payload shown above.

---

## ⚖️ Trade-Offs & Future Improvements

Since this was a scoped assignment (approx. 8 hours), I had to make some specific trade-offs:

* **No Database:** I focused on the logic pipeline. In a production version, I would add a database (like PostgreSQL or Redis) to cache results so we don't pay for the same API call twice.
* **Heuristic Confidence:** The confidence score is currently rule-based. Ideally, this would be calibrated against a "Gold Standard" dataset over time.
* **Latency:** The response time depends heavily on the AI provider. For production, this would likely move to an async queue (Celery/RabbitMQ) rather than a synchronous HTTP request.

---

## 📝 Summary

This project was a great exercise in **systems thinking**. It demonstrates that using AI isn't just about sending a prompt—it's about building a robust architecture around that prompt to ensure the data you get back is actually useful, valid, and safe to use in a business context.