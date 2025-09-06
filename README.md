# LLM-Based Sentiment Marker (Movie Reviews)

This project builds a sentiment marking system for movie reviews using **Google Gemini** LLM.  
It classifies reviews as **Positive**, **Negative**, or **Neutral** and provides a short rationale with evidence phrases.

---

## Features
- **Streamlit Web App** (`streamlit_app.py`): Paste a review → get sentiment label, confidence, explanation, and highlighted evidence phrases.  
- **Batch Evaluation** (`batch_eval.py`): Score a CSV of reviews(used an IMDB dataset of 100 reviews) and save results to `scored_reviews.csv`.  
- **LLM Wrapper** (`sentiment_llm.py`): Handles prompting, caching, and JSON parsing.

## Setup

1. **Clone the repo**

2. **Create a Python environment** 

3. **Install dependencies**
pip install -r requirements.txt


4. **Set your Gemini API key** (never commit it!)
# Linux / Mac
export GOOGLE_API_KEY="your_api_key_here"

# Windows PowerShell
setx GOOGLE_API_KEY "your_api_key_here"

---

## Run the Streamlit App
streamlit run streamlit_app.py


* Select **Lenient** or **Strict** mode.
* Paste a movie review and click **Analyze Review**.
* Evidence phrases will be highlighted in bold.
* Confidence calibration ensures more reliable predictions.

---

## Run Batch Evaluation
python batch_eval.py

* Reads `reviews.csv` (column: `review`), scores each review using Gemini, and saves results to `scored_reviews.csv`.
* Includes **retry/backoff** for API errors and falls back to safe JSON on failures.

---

## Prompt Design Notes

* **JSON-only output** ensures reliable parsing.
* **Evidence phrases** are extracted and shown in bold for clarity.
* **Strict vs Lenient mode**:

  * Strict → classifies as Neutral if sentiment is ambiguous.
  * Lenient → attempts to infer sentiment even if partially clear.
* **Confidence calibration**:

  * If the model’s confidence <0.6, a second pass re-evaluates the review for more reliable output.
* **Temperature**:

  * Strict mode → `temperature=0.0` (deterministic, stable results)
  * Lenient mode → `temperature=0.4` (more natural explanations in UI)
* **Caching** is implemented to avoid repeated API calls, saving cost and latency.

---

## Project Structure
Internship_assign/
- │
- ├─ streamlit_app.py       # Streamlit web UI
- ├─ batch_eval.py          # Batch scoring of reviews
- ├─ sentiment_llm.py       # LLM wrapper & prompt logic
- ├─ requirements.txt       # Python dependencies
- ├─ README.md
- ├─ REPORT.md
- ├─ reviews.csv            # Sample review dataset (input)
- └─ scored_reviews.csv     # LLM scored reviews (output)

## Notes

* Gemini API free tier has **rate limits** — caching helps reduce calls.
* Temperature and prompt design choices balance **determinism** for evaluation vs **natural UI explanations**.


