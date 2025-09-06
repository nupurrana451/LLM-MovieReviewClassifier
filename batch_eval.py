import pandas as pd
import time
from sentiment_llm import analyze_review

def safe_analyze(review, temperature=0.0, max_retries=3):
    """Run analyze_review with retry on errors."""
    for attempt in range(max_retries):
        try:
            return analyze_review(review, temperature=temperature)
        except Exception as e:
            print(f"Error: {e} | Attempt {attempt+1}/{max_retries}")
            
            # Exponential backoff: wait longer after each failure
            wait_time = 10 * (2 ** attempt)
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    # If all retries fail, return fallback JSON
    return {
        "label": "Error",
        "confidence": 0,
        "explanation": f"Failed after {max_retries} retries",
        "evidence_phrases": []
    }

# Main loop
df = pd.read_csv("reviews.csv")  # column: "review"
results = []

for i, r in enumerate(df["review"]):
    result = safe_analyze(r,temperature=0.0)
    results.append(result)

    print(f"Processed {i+1}/{len(df)}")

# Save results
pd.DataFrame(results).to_csv("scored_reviews.csv", index=False)
print("All reviews processed and saved to scored_reviews.csv")

