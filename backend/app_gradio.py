import gradio as gr
from model import predict

def contradiction_detector(sentence_a, sentence_b):
    result = predict(sentence_a, sentence_b)
    label = result["label"]
    confidence = result["confidence"]
    nltk = result["nltk_analysis"]
    
    output = f"""
    **Label:** {label}
    **Confidence:** {confidence:.2%}
    
    **NLTK Analysis:**
    - Token Overlap: {nltk['token_overlap']}
    - WordNet Similarity: {nltk['wordnet_similarity']}
    - Common Tokens: {', '.join(nltk['common_tokens']) if nltk['common_tokens'] else 'None'}
    """
    return output

demo = gr.Interface(
    fn=contradiction_detector,
    inputs=[
        gr.Textbox(label="Sentence A"),
        gr.Textbox(label="Sentence B")
    ],
    outputs="markdown",
    title="🔍 Contradiction Detector",
    description="Determine if two sentences are Consistent, Contradictory, or Unrelated"
)

if __name__ == "__main__":
    demo.launch()