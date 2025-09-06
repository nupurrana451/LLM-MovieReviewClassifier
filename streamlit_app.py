import streamlit as st
from sentiment_llm import analyze_review
import re
import os
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
st.title("Movie Review Sentiment Analyzer")
st.write("Enter a movie review, and the app will analyze its sentiment using a large language model.")
mode=st.radio("Select Mode:",["Lenient","Strict"], horizontal=True)
review = st.text_area("Enter your movie review:", height=200)
if st.button("Analyze Review"):
    if not review.strip():
        st.warning("Please enter a movie review to analyze.")
    else:
        with st.spinner("Analyzing review..."):
            try:
                user_prompt=review
                if mode=="Strict":
                    temperature=0.0
                    user_prompt+="\nBe very strict in your classification. Only classify as Positive if the review is overwhelmingly positive, Negative if overwhelmingly negative, otherwise classify as Neutral."
                else:
                    temperature=0.4
                    user_prompt+="\nClassify the review as Positive, Negative, or Neutral based on its overall sentiment."
                result = analyze_review(user_prompt,)
                if result.get("confidence",0)<0.6:
                    check_prompt=f"Double check the sentiment of this review. If unsure, classify as Neutral.\n\nReview: {review}\n\nCurrent label: {result['label']}, confidence: {result['confidence']}. Is confidence too low? Re-evaluate."
                    check_result=analyze_review(check_prompt)
                    if check_result.get("confidence",0)>result.get("confidence",0):
                        result=check_result
            
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                result = {"label": "Error", "confidence": 0, "explanation": str(e), "evidence_phrases": []}
        st.subheader("Analysis Result")
        st.write(f"**Predicted Sentiment:** {result.get('label', 'N/A')}")
        st.write(f"**Confidence Score:** {result.get('confidence', 'N/A'):.2f}")
        st.write(f"**Explanation:** {result.get('explanation', 'N/A')}")

        if result.get("evidence_phrases"):
            st.markdown("**Evidence Phrases:**")
            highlighted_text=review
            for phrase in result["evidence_phrases"]:
                if phrase.strip():
                    highlighted_text = re.sub(
                        re.escape(phrase),
                        f"**{phrase}**",
                        highlighted_text,
                        flags=re.IGNORECASE
                    )
                    st.markdown(f"- **{phrase}**")
            st.markdown("**Review with Highlighted Evidence Phrases:**")
            st.markdown(highlighted_text)
        with st.expander("Full JSON Response"):
            st.json(result)

            
        


