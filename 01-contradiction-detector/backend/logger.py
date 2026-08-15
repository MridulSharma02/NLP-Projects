import json
import csv
import os
from datetime import datetime

LOG_FILE_JSON = "logs/predictions.json"
LOG_FILE_CSV = "logs/predictions.csv"

os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG_FILE_CSV):
    with open(LOG_FILE_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "sentence_a", "sentence_b",
            "label", "confidence",
            "token_overlap", "antonyms_found", "wordnet_similarity"
        ])


def log_prediction(sentence_a: str, sentence_b: str, result: dict):
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "sentence_a": sentence_a,
        "sentence_b": sentence_b,
        "label": result["label"],
        "confidence": result["confidence"],
        "nltk_analysis": result["nltk_analysis"]
    }
    logs = []
    if os.path.exists(LOG_FILE_JSON):
        with open(LOG_FILE_JSON, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(entry)
    with open(LOG_FILE_JSON, "w") as f:
        json.dump(logs, f, indent=2)

    with open(LOG_FILE_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp, sentence_a, sentence_b,
            result["label"], result["confidence"],
            result["nltk_analysis"]["token_overlap"],
            "; ".join(result["nltk_analysis"]["antonyms_found"]),
            result["nltk_analysis"]["wordnet_similarity"]
        ])


def get_stats() -> dict:
    if not os.path.exists(LOG_FILE_JSON):
        return {"total_predictions": 0, "label_distribution": {}, "average_confidence": 0.0}
    with open(LOG_FILE_JSON, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    if not logs:
        return {"total_predictions": 0, "label_distribution": {}, "average_confidence": 0.0}
    total = len(logs)
    label_counts = {}
    confidence_sum = 0.0
    for entry in logs:
        label = entry["label"]
        label_counts[label] = label_counts.get(label, 0) + 1
        confidence_sum += entry["confidence"]
    return {
        "total_predictions": total,
        "label_distribution": label_counts,
        "average_confidence": round(confidence_sum / total, 4)
    }
