import pandas as pd
import re
import os

CLEAN_DIR = "data/cleaned"
RESULTS_DIR = "data/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Common informal/abbreviated patterns in crisis messages
INFORMAL_PATTERNS = {
    "abbreviations": [
        (r'\bplz\b', 'please'), (r'\bpls\b', 'please'), (r'\bu\b', 'you'),
        (r'\br\b', 'are'), (r'\bwth\b', 'what'), (r'\bhlp\b', 'help'),
        (r'\bsnd\b', 'send'), (r'\bnd\b', 'and'), (r'\bbc\b', 'because'),
        (r'\basap\b', 'as soon as possible'), (r'\bbtw\b', 'by the way'),
        (r'\bidk\b', 'i do not know'), (r'\bomg\b', 'oh my god'),
        (r'\bwtf\b', 'what the'), (r'\bbrb\b', 'be right back'),
        (r'\b2\b', 'to'), (r'\b4\b', 'for'), (r'\bb4\b', 'before'),
        (r'\bgr8\b', 'great'), (r'\bthx\b', 'thanks'), (r'\bthnx\b', 'thanks'),
    ],
    "repeated_chars": [
        r'\b\w*(.)\1{2,}\w*\b',   # helppp, urgenttt
    ],
    "missing_spaces": [
        r'[a-z][A-Z]',            # camelCase without space
    ],
    "all_caps": [
        r'\b[A-Z]{3,}\b',         # SOS, URGENT, HELP
    ],
    "number_words": [
        r'\d+(?=[a-zA-Z])',       # 2help, 4food, no1
    ],
}

def detect_patterns(text):
    text = str(text)
    findings = {}

    # Abbreviations found
    abbrevs = []
    for pattern, replacement in INFORMAL_PATTERNS["abbreviations"]:
        if re.search(pattern, text, re.IGNORECASE):
            match = re.search(pattern, text, re.IGNORECASE)
            abbrevs.append(f"{match.group()} → {replacement}")
    findings["abbreviations"] = abbrevs

    # Repeated chars
    repeated = re.findall(r'\b\w*(.)\1{2,}\w*\b', text)
    findings["repeated_chars"] = list(set(repeated))

    # ALL CAPS words
    caps = re.findall(r'\b[A-Z]{3,}\b', text)
    findings["all_caps"] = caps

    # Number-word combos
    numwords = re.findall(r'\d+[a-zA-Z]+|[a-zA-Z]+\d+', text)
    findings["number_words"] = numwords

    # Multiple punctuation
    multi_punct = re.findall(r'[!?]{2,}', text)
    findings["multi_punct"] = multi_punct

    is_informal = bool(abbrevs or repeated or numwords or multi_punct)
    return findings, is_informal

def main():
    print("=" * 60)
    print("  EMERGENCY CORPUS — SPELL & PATTERN CHECK")
    print("=" * 60)

    df = pd.read_csv(f"{CLEAN_DIR}/cleaned.csv")
    # Use sample for speed
    sample = df.sample(min(1000, len(df)), random_state=42).copy()
    print(f"Analyzing {len(sample)} messages for informal patterns...")

    results = []
    abbrev_total, caps_total, numword_total, punct_total = 0, 0, 0, 0

    for _, row in sample.iterrows():
        findings, informal = detect_patterns(row["text"])
        abbrev_total += len(findings["abbreviations"])
        caps_total += len(findings["all_caps"])
        numword_total += len(findings["number_words"])
        punct_total += len(findings["multi_punct"])
        results.append({
            "text": row["text"],
            "abbreviations": "|".join(findings["abbreviations"]),
            "all_caps": "|".join(findings["all_caps"]),
            "number_words": "|".join(findings["number_words"]),
            "multi_punct": "|".join(findings["multi_punct"]),
            "is_informal": informal,
        })

    out = pd.DataFrame(results)
    out.to_csv(f"{RESULTS_DIR}/spell_check.csv", index=False)

    print(f"\n✔ Spell check results saved to {RESULTS_DIR}/spell_check.csv")
    print(f"\n── Pattern Summary (from {len(sample)} messages) ──")
    print(f"  Abbreviations found:      {abbrev_total}")
    print(f"  ALL CAPS words:           {caps_total}")
    print(f"  Number-word combos:       {numword_total}")
    print(f"  Multi-punctuation (!!, ??): {punct_total}")
    print(f"  Informal messages:        {out['is_informal'].sum()}")

    print(f"\n── Sample Informal Messages ──")
    informal_samples = out[out["is_informal"]].head(5)
    for _, row in informal_samples.iterrows():
        print(f"  TEXT: {row['text'][:80]}")
        if row["abbreviations"]:
            print(f"    Abbrevs: {row['abbreviations'][:60]}")
        if row["all_caps"]:
            print(f"    CAPS:    {row['all_caps'][:60]}")
        print()

    print("✔ Spell check complete!")

if __name__ == "__main__":
    main()