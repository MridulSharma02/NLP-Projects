import pandas as pd
import spacy
import re
import os

nlp = spacy.load("en_core_web_sm")

CLEAN_DIR = "data/cleaned"
RESULTS_DIR = "data/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# ── Location syntactic patterns ───────────────────────────────────────────────
LOCATION_SYNTACTIC = [
    (r'\b(near|in|at|around|toward|towards|from)\s+[A-Z][a-zA-Z\s]{2,20}', "PREP+PROPN"),
    (r'\b(road|highway|NH|street|district|village|city|town|area|sector|zone|port|beach|river|coast|station|bridge)\b', "LOC_NOUN"),
    (r'\bNH\s*\d+\b', "HIGHWAY_CODE"),
    (r'\bsector\s+\d+\b', "SECTOR_NUM"),
    (r'\b[A-Z][a-z]+\s+(district|village|city|town|area|zone|coast|river|beach)\b', "PROPN+LOC_NOUN"),
]

# ── Action syntactic patterns ─────────────────────────────────────────────────
ACTION_SYNTACTIC = [
    (r'\b(send|need|require|evacuate|rescue|help|assist|deploy|call|donate|move|escape|flee|save)\b', "ACTION_VERB"),
    (r'\b(SOS|URGENT|MAYDAY|EMERGENCY)\b', "DISTRESS_SIGNAL"),
    (r'\b(immediately|asap|urgently|now|quick|fast)\b', "URGENCY_ADVERB"),
    (r'\bplease\s+(help|send|call|rescue|assist|come)\b', "PLEA_PATTERN"),
    (r'\bneed\s+(help|rescue|food|water|medicine|shelter|boats?|helicopters?)\b', "NEED+RESOURCE"),
    (r'\b(trapped|stuck|stranded|unconscious|injured|missing)\b', "VICTIM_STATE"),
]

def extract_syntactic_patterns(text, doc):
    results = {"location_patterns": [], "action_patterns": [], "dep_patterns": []}

    # Regex-based pattern detection
    for pattern, label in LOCATION_SYNTACTIC:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            results["location_patterns"].append(label)

    for pattern, label in ACTION_SYNTACTIC:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            results["action_patterns"].append(label)

    # spaCy dependency patterns
    for token in doc:
        # VERB → dobj pattern (send help, need rescue)
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            children = [c.text for c in token.children]
            results["dep_patterns"].append(f"ROOT_VERB:{token.text}")

        # prep → pobj (near X, in X, at X)
        if token.dep_ == "prep" and token.head.pos_ in ("VERB", "NOUN"):
            pobj = [c for c in token.children if c.dep_ == "pobj"]
            if pobj:
                results["dep_patterns"].append(f"PREP({token.text})+POBJ({pobj[0].text})")

        # NER locations
        if token.ent_type_ in ("GPE", "LOC", "FAC"):
            results["dep_patterns"].append(f"NER_LOC:{token.text}")

    return results

def main():
    print("=" * 60)
    print("  EMERGENCY CORPUS — SYNTACTIC PATTERN DETECTION")
    print("=" * 60)

    df = pd.read_csv(f"{CLEAN_DIR}/cleaned.csv")
    sample = df.sample(min(2000, len(df)), random_state=42).copy()
    print(f"Analyzing {len(sample)} messages for syntactic patterns...")

    rows = []
    loc_pattern_counts = {}
    act_pattern_counts = {}
    dep_pattern_counts = {}

    for i, (_, row) in enumerate(sample.iterrows()):
        text = str(row["text"])
        doc = nlp(text)
        res = extract_syntactic_patterns(text, doc)

        for lp in res["location_patterns"]:
            loc_pattern_counts[lp] = loc_pattern_counts.get(lp, 0) + 1
        for ap in res["action_patterns"]:
            act_pattern_counts[ap] = act_pattern_counts.get(ap, 0) + 1
        for dp in set(res["dep_patterns"]):
            key = dp.split(":")[0]
            dep_pattern_counts[key] = dep_pattern_counts.get(key, 0) + 1

        rows.append({
            "text": text,
            "disaster_type": row.get("disaster_type", "unknown"),
            "location_patterns": "|".join(set(res["location_patterns"])),
            "action_patterns": "|".join(set(res["action_patterns"])),
            "dep_patterns": "|".join(res["dep_patterns"][:5]),
            "has_location": len(res["location_patterns"]) > 0,
            "has_action": len(res["action_patterns"]) > 0,
        })

        if (i + 1) % 500 == 0:
            print(f"  ... {i+1} done")

    out = pd.DataFrame(rows)
    out.to_csv(f"{RESULTS_DIR}/pattern_detect.csv", index=False)

    print(f"\n✔ Pattern detection saved to {RESULTS_DIR}/pattern_detect.csv")
    print(f"\n── Location Pattern Frequency ──")
    for k, v in sorted(loc_pattern_counts.items(), key=lambda x: -x[1]):
        print(f"  {k:<25} {v}")

    print(f"\n── Action Pattern Frequency ──")
    for k, v in sorted(act_pattern_counts.items(), key=lambda x: -x[1]):
        print(f"  {k:<25} {v}")

    print(f"\n── Dependency Pattern Frequency ──")
    for k, v in sorted(dep_pattern_counts.items(), key=lambda x: -x[1])[:8]:
        print(f"  {k:<25} {v}")

    print(f"\n── Coverage ──")
    print(f"  Messages with location pattern: {out['has_location'].sum()} ({round(out['has_location'].mean()*100,1)}%)")
    print(f"  Messages with action pattern:   {out['has_action'].sum()} ({round(out['has_action'].mean()*100,1)}%)")
    print("\n✔ Pattern detection complete!")

if __name__ == "__main__":
    main()