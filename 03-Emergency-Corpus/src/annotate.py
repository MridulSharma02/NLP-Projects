import pandas as pd
import spacy
import re
import os

nlp = spacy.load("en_core_web_sm")

RAW_DIR = "data/raw"
ANNOTATED_DIR = "data/annotated"
os.makedirs(ANNOTATED_DIR, exist_ok=True)

# ── Location patterns ─────────────────────────────────────────────────────────
LOCATION_PATTERNS = [
    r'\bnear\s+[A-Z][a-zA-Z\s]+',
    r'\bin\s+[A-Z][a-zA-Z\s]+',
    r'\bat\s+[A-Z][a-zA-Z\s]+',
    r'\bnear\s+[a-zA-Z\s]+(?:road|highway|NH|station|district|village|city|town|area|sector|zone|port|beach|river|coast)',
]

# ── Action patterns ───────────────────────────────────────────────────────────
ACTION_PATTERNS = [
    r'\b(send|need|require|evacuate|rescue|help|assist|deploy|call|donate|move|escape|flee)\b',
    r'\b(SOS|urgent|immediately|asap|emergency|please help)\b',
]

def extract_locations(text, doc):
    locations = []
    # spaCy NER
    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC", "FAC"):
            locations.append(ent.text)
    # regex fallback
    for pat in LOCATION_PATTERNS:
        matches = re.findall(pat, text)
        locations.extend([m.strip() for m in matches])
    return list(set(locations))

def extract_actions(text):
    actions = []
    text_lower = text.lower()
    for pat in ACTION_PATTERNS:
        matches = re.findall(pat, text_lower, re.IGNORECASE)
        actions.extend(matches)
    return list(set(actions))

def detect_urgency(text):
    urgent_words = ["sos", "urgent", "immediately", "asap", "trapped", "help", "emergency", "now", "please"]
    text_lower = text.lower()
    score = sum(1 for w in urgent_words if w in text_lower)
    if score >= 3:
        return "high"
    elif score >= 1:
        return "medium"
    return "low"

def detect_informal(text):
    informal_signals = [
        r'\b\w*(nd|wth|plz|pls|hlp|rly|evry|cmng)\b',
        r'\d+(?=\w)',   # numbers attached to words like "no1"
        r'[!]{2,}',     # multiple exclamation marks
        r'[A-Z]{3,}',   # ALL CAPS words
    ]
    for pat in informal_signals:
        if re.search(pat, text):
            return True
    return False

def annotate(text):
    doc = nlp(str(text))
    tokens = [t.text for t in doc]
    pos_tags = [t.pos_ for t in doc]
    locations = extract_locations(str(text), doc)
    actions = extract_actions(str(text))
    urgency = detect_urgency(str(text))
    informal = detect_informal(str(text))
    sentence_count = len(list(doc.sents))
    word_count = len([t for t in doc if not t.is_space])
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "locations": "|".join(locations),
        "location_count": len(locations),
        "actions": "|".join(actions),
        "action_count": len(actions),
        "urgency_level": urgency,
        "is_informal": informal,
        "pos_tags": " ".join(pos_tags),
    }

def main():
    print("=" * 60)
    print("  EMERGENCY CORPUS — ANNOTATION")
    print("=" * 60)

    df = pd.read_csv(f"{RAW_DIR}/all_raw.csv")
    print(f"Loaded {len(df)} messages.")

    # Sample for speed: 5000 HumAID + all manual
    humaid = df[df["source"] == "HumAID"].sample(5000, random_state=42)
    manual = df[df["source"] == "manual"]
    df_sample = pd.concat([humaid, manual], ignore_index=True)
    print(f"Annotating {len(df_sample)} messages (5000 HumAID + {len(manual)} manual)...")

    results = []
    for i, row in df_sample.iterrows():
        ann = annotate(row["text"])
        ann["text"] = row["text"]
        ann["disaster_type"] = row["disaster_type"]
        ann["source"] = row["source"]
        results.append(ann)
        if (len(results)) % 500 == 0:
            print(f"  ... {len(results)} done")

    out = pd.DataFrame(results)
    out.to_csv(f"{ANNOTATED_DIR}/annotated.csv", index=False)
    print(f"\n✔ Annotated {len(out)} messages saved to {ANNOTATED_DIR}/annotated.csv")
    print("\nUrgency distribution:")
    print(out["urgency_level"].value_counts().to_string())
    print("\nTop disaster types:")
    print(out["disaster_type"].value_counts().head(10).to_string())
    print("\n✔ Annotation complete!")

if __name__ == "__main__":
    main()