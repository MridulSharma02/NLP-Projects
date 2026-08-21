import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')

import spaces
import gradio as gr
from model import predict

EXAMPLES = [
    ["The cat is sleeping on the bed", "The cat is wide awake and running outside"],
    ["She drinks coffee every morning", "She has a daily morning coffee routine"],
    ["The stock market crashed today", "I love eating pizza on weekends"],
    ["He sometimes skips breakfast", "He never eats in the morning"],
]

EMOJI_MAP = {"Contradiction": "❌", "Consistent": "✅", "Unrelated": "↔️"}
COLOR_MAP = {"Contradiction": "#ff4b4b", "Consistent": "#00cc44", "Unrelated": "#888888"}

@spaces.GPU
def contradiction_detector(sentence_a, sentence_b):
    if not sentence_a.strip() or not sentence_b.strip():
        return "⚠️ Please enter both sentences."
    result = predict(sentence_a, sentence_b)
    label = result["label"]
    confidence = result["confidence"]
    nltk_data = result["nltk_analysis"]
    emoji = EMOJI_MAP.get(label, "")
    color = COLOR_MAP.get(label, "#888888")
    common = ', '.join(nltk_data['common_tokens']) if nltk_data['common_tokens'] else 'None'
    output = f"""
<div style="background:#1e1e2e;border-radius:12px;padding:20px;font-family:sans-serif;">
  <div style="font-size:1.6em;font-weight:bold;color:{color};margin-bottom:8px;">
    {emoji} {label}
  </div>
  <div style="color:#aaa;font-size:0.95em;margin-bottom:16px;">
    Confidence: <strong style="color:white;">{confidence:.2%}</strong>
  </div>
  <hr style="border-color:#333;margin-bottom:16px;">
  <div style="color:#ccc;font-size:0.9em;">
    <strong style="color:white;">NLTK Analysis</strong><br><br>
    🔤 <b>Token Overlap:</b> {nltk_data['token_overlap']}<br>
    🔗 <b>WordNet Similarity:</b> {nltk_data['wordnet_similarity']}<br>
    📌 <b>Common Tokens:</b> {common}
  </div>
</div>
"""
    return output

with gr.Blocks(theme=gr.themes.Soft(), title="Contradiction Detector") as demo:
    gr.Markdown("# 🔍 Contradiction Detector")
    gr.Markdown("Analyze whether two sentences are **Consistent**, **Contradictory**, or **Unrelated** using NLP + deep learning.")

    with gr.Row():
        sentence_a = gr.Textbox(label="Sentence A", placeholder="Enter first sentence...", lines=3)
        sentence_b = gr.Textbox(label="Sentence B", placeholder="Enter second sentence...", lines=3)

    with gr.Row():
        clear_btn = gr.Button("🗑️ Clear", variant="secondary")
        analyze_btn = gr.Button("🔍 Analyze", variant="primary")

    output = gr.HTML()

    gr.Markdown("### 💡 Try an Example")
    gr.Examples(
        examples=EXAMPLES,
        inputs=[sentence_a, sentence_b],
        label="Click any example to load it"
    )

    analyze_btn.click(fn=contradiction_detector, inputs=[sentence_a, sentence_b], outputs=output)
    clear_btn.click(fn=lambda: ("", "", ""), outputs=[sentence_a, sentence_b, output])

demo.launch()