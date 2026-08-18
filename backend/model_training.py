from datasets import load_dataset
from sentence_transformers import CrossEncoder
import torch

def train_and_save_model():
    print("Loading SNLI dataset...")
    dataset = load_dataset("stanfordnlp/snli", split="train")
    dataset = dataset.filter(lambda x: x["label"] != -1).select(range(5000))  # 5k samples
    
    print("Loading base model...")
    model = CrossEncoder("cross-encoder/nli-deberta-v3-small")
    
    print("Fine-tuning on SNLI...")
    train_samples = []
    for sample in dataset:
        train_samples.append({
            "texts": [sample["premise"], sample["hypothesis"]],
            "label": sample["label"]
        })
    
    model.fit(
        train_objectives=[(train_samples, None)],
        epochs=1,
        batch_size=32,
        warmup_steps=100,
        output_path="./fine-tuned-model"
    )
    print("Model saved to ./fine-tuned-model")

if __name__ == "__main__":
    train_and_save_model()