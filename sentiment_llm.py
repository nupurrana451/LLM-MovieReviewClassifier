import google.generativeai as genai
import os
import json
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_review(review: str):
    prompt = f"""
    Analyze the following movie review.
    Classify this review as Positive, Negative, or Neutral. 
    Respond ONLY in valid JSON with these fields:
    {{
      "label": "Positive | Negative | Neutral",
      "confidence": 0.00,
      "explanation": "Short reason grounded in the text",
      "evidence_phrases": ["phrase1", "phrase2"]
    }}

    Review: {review}
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    text = response.text.strip()

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {
        "label": "Error",
        "confidence": 0.0,
        "explanation": "Parsing failed",
        "evidence_phrases": []
    }
