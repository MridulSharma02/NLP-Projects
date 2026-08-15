from datasets import load_dataset
from model import predict
from sklearn.metrics import classification_report, confusion_matrix
import json
import os

os.makedirs("logs", exist_ok=True)

SNLI_LABEL_MAP = {0: "Consistent", 1: "Unrelated", 2: "Contradiction"}

def run_evaluation(num_samples: int = 100):
    print(f"Loading {num_samples} samples from SNLI...")
    dataset = load_dataset("stanfordnlp/snli", split="test")
    dataset = dataset.filter(lambda x: x["label"] != -1)
    samples = dataset.select(range(num_samples))

    true_labels, pred_labels, results = [], [], []

    for i, sample in enumerate(samples):
        sentence_a = sample["premise"]
        sentence_b = sample["hypothesis"]
        true_label = SNLI_LABEL_MAP[sample["label"]]
        result = predict(sentence_a, sentence_b)
        pred_label = result["label"]

        true_labels.append(true_label)
        pred_labels.append(pred_label)
        results.append({
            "sentence_a": sentence_a,
            "sentence_b": sentence_b,
            "true_label": true_label,
            "predicted_label": pred_label,
            "confidence": result["confidence"],
            "correct": true_label == pred_label
        })
        print(f"[{i+1}/{num_samples}] True: {true_label} | Pred: {pred_label} | Conf: {result['confidence']}")

    with open("logs/evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n========== CLASSIFICATION REPORT ==========")
    print(classification_report(true_labels, pred_labels))

    labels = ["Contradiction", "Consistent", "Unrelated"]
    cm = confusion_matrix(true_labels, pred_labels, labels=labels)
    print("========== CONFUSION MATRIX ==========")
    print(f"{'':>15}", " ".join(f"{l:>15}" for l in labels))
    for label, row in zip(labels, cm):
        print(f"{label:>15}", " ".join(f"{v:>15}" for v in row))

    correct = sum(1 for r in results if r["correct"])
    print(f"\nAccuracy: {correct}/{num_samples} = {round(correct/num_samples*100, 2)}%")
    print("Results saved to logs/evaluation_results.json")


if __name__ == "__main__":
    run_evaluation(num_samples=100)
