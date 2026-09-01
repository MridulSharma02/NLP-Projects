from datasets import load_dataset
import pandas as pd

print("Downloading dataset...")
dataset = load_dataset("tatsu-lab/alpaca", split="train[:2000]")

print("Processing...")
rows = []
for item in dataset:
    rows.append({"speaker": "human", "text": item["instruction"]})
    rows.append({"speaker": "ai", "text": item["output"]})

df = pd.DataFrame(rows)
df.to_csv("corpus_raw.csv", index=False)
print(f"Done! Saved {len(df)} rows to corpus_raw.csv")