from sentence_transformers import CrossEncoder
from preprocessor import analyze

model = CrossEncoder("cross-encoder/nli-deberta-v3-small")

LABELS = {0: "Contradiction", 1: "Entailment", 2: "Neutral"}
LABEL_MAP = {"Contradiction": "Contradiction", "Entailment": "Consistent", "Neutral": "Unrelated"}


def predict(sentence_a: str, sentence_b: str) -> dict:
    nltk_data = analyze(sentence_a, sentence_b)
    scores = model.predict(
        [(sentence_a, sentence_b)],
        apply_softmax=True
    )[0]
    predicted_index = int(scores.argmax())
    raw_label = LABELS[predicted_index]
    # Override: if model says Contradiction but NLTK shows no connection, it's Unrelated
    final_label = LABEL_MAP[raw_label]
    if final_label == "Contradiction" and nltk_data["token_overlap"] == 0.0 and nltk_data["wordnet_similarity"] < 0.15:
        final_label = "Unrelated"
    return {
        "label": final_label,
        "confidence": round(float(scores[predicted_index]), 4),
        "nltk_analysis": {
            "cleaned_a": nltk_data["cleaned_a"],
            "cleaned_b": nltk_data["cleaned_b"],
            "token_overlap": nltk_data["token_overlap"],
            "common_tokens": nltk_data["common_tokens"],
            "antonyms_found": nltk_data["antonyms_found"],
            "wordnet_similarity": nltk_data["wordnet_similarity"],
        }
    }


def predict_batch(pairs: list[dict]) -> list[dict]:
    return [predict(p["sentence_a"], p["sentence_b"]) for p in pairs]
