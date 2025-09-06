import google.generativeai as genai
import os
import json
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

CACHE_FILE="sentiment_cache.json"
cache={}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE,"r") as f:
        try:
            cache=json.load(f)
        except json.JSONDecodeError:
            cache={}

def analyze_review(review: str,temperature: float = 0.0):
    if review in cache and str(temperature) in cache[review]:
        return cache[review][str(temperature)]
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
    response = model.generate_content(prompt,generation_config={"temperature": temperature})

    text = response.text.strip()

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            result = {
                "label": "Error",
                "confidence": 0,
                "explanation": "Failed to parse JSON",
                "evidence_phrases": []
            }
    else:
        result = {
            "label": "Error",
            "confidence": 0,
            "explanation": "No JSON found in response",
            "evidence_phrases": []
        }

    if review not in cache:
        cache[review] = {}
    cache[review][str(temperature)] = result
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    return result
