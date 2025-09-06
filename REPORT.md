# Mini Report: LLM-Based Sentiment Marker (Movie Reviews)

## 1. Prompt Design Choices
- **JSON-only output**: Ensures easy parsing into `label`, `confidence`, `explanation`, `evidence_phrases`.
- **Evidence phrases**: Extracted and highlighted in UI to show rationale.
- **Strict vs Lenient Mode**:
  - **Strict**: Classifies as Neutral if sentiment is ambiguous; deterministic (`temperature=0.0`).
  - **Lenient**: Attempts to infer sentiment even if partially clear; more natural responses (`temperature=0.4`).
- **Confidence Calibration**: If model’s confidence <0.6, a second-pass check re-evaluates the review.
- **Few-shot prompting** (example included in prompt for guidance):

**Input Review:**  
*"The acting was fantastic but the story was weak."*

**Expected JSON Response:**  
{
  "label": "Neutral",
  "confidence": 0.75,
  "explanation": "The acting is praised, but the story is criticized, giving a mixed overall sentiment.",
  "evidence_phrases": ["acting was fantastic", "story was weak"]
}

## 2. Failure Cases & Mitigation
- Low-confidence predictions-->Confidence calibration(second pass)
- Neutral class misclassified-->Strict mode favors neutral for ambiguous reviews
- API rate limits / transient errors-->Retry + exponential backoff in batch_eval.py; caching to reduce repeated calls.

## 3. Mini Metrics Table (Test Set)

| Class    | True Count | Predicted Count |
| -------- | ---------- | --------------- |
| Positive | 40         | 36              |
| Negative | 56         | 60              |
| Neutral  | 3          | 3               |

# **Overall Accuracy:** 0.94

> Note: Dataset contains mostly Positive/Negative reviews; Neutral is underrepresented. Metrics are approximate due to LLM subjectivity.

