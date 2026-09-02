import pandas as pd
import json
import os

ANNOTATED_DIR = "data/annotated"
RESULTS_DIR = "data/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def main():
    print("=" * 60)
    print("  EMERGENCY CORPUS — ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(f"{ANNOTATED_DIR}/annotated.csv")
    print(f"Loaded {len(df)} annotated messages.")

    results = {}

    # ── 1. Basic corpus stats ─────────────────────────────────────────────────
    results["corpus_stats"] = {
        "total_messages": len(df),
        "avg_word_count": round(df["word_count"].mean(), 2),
        "avg_sentence_count": round(df["sentence_count"].mean(), 2),
        "avg_location_count": round(df["location_count"].mean(), 2),
        "avg_action_count": round(df["action_count"].mean(), 2),
        "messages_with_location": int((df["location_count"] > 0).sum()),
        "messages_with_action": int((df["action_count"] > 0).sum()),
        "informal_messages": int(df["is_informal"].sum()),
    }
    print("\n[1/5] Corpus stats done.")

    # ── 2. Disaster type distribution ─────────────────────────────────────────
    results["disaster_type_distribution"] = df["disaster_type"].value_counts().to_dict()
    print("[2/5] Disaster type distribution done.")

    # ── 3. Urgency distribution ───────────────────────────────────────────────
    results["urgency_distribution"] = df["urgency_level"].value_counts().to_dict()

    # Urgency by disaster type
    urgency_by_type = df.groupby("disaster_type")["urgency_level"].value_counts().unstack(fill_value=0)
    results["urgency_by_disaster_type"] = urgency_by_type.to_dict()
    print("[3/5] Urgency analysis done.")

    # ── 4. Location & action analysis ─────────────────────────────────────────
    # Most common actions
    all_actions = []
    for actions in df["actions"].dropna():
        all_actions.extend([a for a in actions.split("|") if a])
    action_freq = pd.Series(all_actions).value_counts().head(15).to_dict()
    results["top_actions"] = action_freq

    # Messages with locations by disaster type
    loc_by_type = df[df["location_count"] > 0].groupby("disaster_type").size().to_dict()
    results["location_mentions_by_type"] = loc_by_type
    print("[4/5] Location & action analysis done.")

    # ── 5. Syntactic patterns (POS) ───────────────────────────────────────────
    # POS tag frequency across corpus
    all_pos = []
    for pos_str in df["pos_tags"].dropna():
        all_pos.extend(pos_str.split())
    pos_freq = pd.Series(all_pos).value_counts().to_dict()
    results["pos_distribution"] = pos_freq

    # Compare POS patterns: high urgency vs low urgency
    high_pos, low_pos = [], []
    for _, row in df.iterrows():
        tags = str(row["pos_tags"]).split()
        if row["urgency_level"] == "high":
            high_pos.extend(tags)
        elif row["urgency_level"] == "low":
            low_pos.extend(tags)

    high_pos_freq = pd.Series(high_pos).value_counts(normalize=True).round(4).to_dict()
    low_pos_freq = pd.Series(low_pos).value_counts(normalize=True).round(4).to_dict()
    results["pos_high_urgency"] = high_pos_freq
    results["pos_low_urgency"] = low_pos_freq
    print("[5/5] Syntactic pattern analysis done.")

    # ── Word count by disaster type ───────────────────────────────────────────
    wc_by_type = df.groupby("disaster_type")["word_count"].mean().round(2).to_dict()
    results["avg_word_count_by_type"] = wc_by_type

    # ── Informal vs formal stats ──────────────────────────────────────────────
    informal_df = df[df["is_informal"] == True]
    formal_df = df[df["is_informal"] == False]
    results["informal_vs_formal"] = {
        "informal_count": len(informal_df),
        "formal_count": len(formal_df),
        "informal_avg_words": round(informal_df["word_count"].mean(), 2),
        "formal_avg_words": round(formal_df["word_count"].mean(), 2),
        "informal_avg_actions": round(informal_df["action_count"].mean(), 2),
        "formal_avg_actions": round(formal_df["action_count"].mean(), 2),
    }

    # ── Save results ──────────────────────────────────────────────────────────
    with open(f"{RESULTS_DIR}/analysis.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✔ Analysis saved to {RESULTS_DIR}/analysis.json")
    print("\n── Key Findings ──────────────────────────────────────────")
    print(f"  Total messages:        {results['corpus_stats']['total_messages']}")
    print(f"  Avg words/message:     {results['corpus_stats']['avg_word_count']}")
    print(f"  With location mention: {results['corpus_stats']['messages_with_location']}")
    print(f"  With action word:      {results['corpus_stats']['messages_with_action']}")
    print(f"  Informal messages:     {results['corpus_stats']['informal_messages']}")
    print(f"  Top action words:      {list(action_freq.keys())[:5]}")
    print("\n✔ Analysis complete!")

if __name__ == "__main__":
    main()