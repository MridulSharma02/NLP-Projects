import streamlit as st
import requests

st.set_page_config(page_title="Contradiction Detector", page_icon="🔍")
st.title("🔍 Contradiction Detector")
st.write("Enter two sentences to check if they are Consistent, Contradictory, or Unrelated.")

sentence_a = st.text_area("Sentence A", placeholder="e.g. The server is running.")
sentence_b = st.text_area("Sentence B", placeholder="e.g. The server is offline.")

if st.button("Analyze"):
    if not sentence_a.strip() or not sentence_b.strip():
        st.warning("Please enter both sentences.")
    else:
        with st.spinner("Analyzing..."):
            response = requests.post(
                "http://localhost:8000/predict",
                json={"sentence_a": sentence_a, "sentence_b": sentence_b}
            )
            result = response.json()

        label = result["label"]
        confidence = result["confidence"]
        nltk = result["nltk_analysis"]

        color = {"Contradiction": "🔴", "Consistent": "🟢", "Unrelated": "🟡"}
        st.markdown(f"## {color[label]} {label}")
        st.metric("Confidence", f"{round(confidence * 100, 2)}%")

        st.divider()
        st.subheader("🔬 NLTK Analysis")
        col1, col2 = st.columns(2)
        col1.metric("Token Overlap", nltk["token_overlap"])
        col2.metric("WordNet Similarity", nltk["wordnet_similarity"])

        if nltk["common_tokens"]:
            st.write("**Common Tokens:**", ", ".join(nltk["common_tokens"]))
        if nltk["antonyms_found"]:
            st.write("**Antonyms Found:**", ", ".join(nltk["antonyms_found"]))