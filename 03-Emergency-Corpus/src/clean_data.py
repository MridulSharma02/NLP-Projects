import pandas as pd
import re
import os

RAW_DIR = "data/raw"
CLEAN_DIR = "data/cleaned"
os.makedirs(CLEAN_DIR, exist_ok=True)

def clean_text(text):
    text = str(text)
    text = re.sub(r'http\S+|www\S+', '', text)       # remove URLs
    text = re.sub(r'@\w+', '', text)                  # remove @mentions
    text = re.sub(r'#(\w+)', r'\1', text)             # strip # but keep word
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)       # remove non-ASCII
    text = re.sub(r'\s+', ' ', text).strip()          # collapse whitespace
    return text

def main():
    print("=" * 60)
    print("  EMERGENCY CORPUS — DATA CLEANING")
    print("=" * 60)

    df = pd.read_csv(f"{RAW_DIR}/all_raw.csv")
    print(f"Loaded {len(df)} raw messages.")

    df["text_clean"] = df["text"].apply(clean_text)
    df = df[df["text_clean"].str.len() > 10]
    df.reset_index(drop=True, inplace=True)

    df.to_csv(f"{CLEAN_DIR}/cleaned.csv", index=False)
    print(f"✔ Cleaned {len(df)} messages saved to {CLEAN_DIR}/cleaned.csv")

if __name__ == "__main__":
    main()