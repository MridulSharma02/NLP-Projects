import pandas as pd
import json
import os

RESULTS_DIR = "data/results"
OUTPUT_DIR = "output"
os.makedirs(f"{OUTPUT_DIR}/figures", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/stats", exist_ok=True)

def main():
    # ── Load analysis results ─────────────────────────────────────────────────
    with open(f"{RESULTS_DIR}/analysis.json") as f:
        analysis = json.load(f)

    # ── Save stats as text summaries ──────────────────────────────────────────
    with open(f"{OUTPUT_DIR}/stats/corpus_stats.txt", "w") as f:
        cs = analysis["corpus_stats"]
        f.write("EMERGENCY CORPUS — STATISTICS SUMMARY\n")
        f.write("=" * 40 + "\n")
        for k, v in cs.items():
            f.write(f"{k}: {v}\n")

    with open(f"{OUTPUT_DIR}/stats/urgency_distribution.txt", "w") as f:
        f.write("URGENCY DISTRIBUTION\n")
        f.write("=" * 40 + "\n")
        for k, v in analysis["urgency_distribution"].items():
            f.write(f"{k}: {v}\n")

    with open(f"{OUTPUT_DIR}/stats/top_actions.txt", "w") as f:
        f.write("TOP ACTION WORDS\n")
        f.write("=" * 40 + "\n")
        for k, v in analysis["top_actions"].items():
            f.write(f"{k}: {v}\n")

    with open(f"{OUTPUT_DIR}/stats/disaster_type_distribution.txt", "w") as f:
        f.write("DISASTER TYPE DISTRIBUTION\n")
        f.write("=" * 40 + "\n")
        for k, v in analysis["disaster_type_distribution"].items():
            f.write(f"{k}: {v}\n")

    with open(f"{OUTPUT_DIR}/stats/informal_vs_formal.txt", "w") as f:
        f.write("INFORMAL VS FORMAL ANALYSIS\n")
        f.write("=" * 40 + "\n")
        for k, v in analysis["informal_vs_formal"].items():
            f.write(f"{k}: {v}\n")

    # ── Save pattern detection summary ────────────────────────────────────────
    pat_df = pd.read_csv(f"{RESULTS_DIR}/pattern_detect.csv")
    with open(f"{OUTPUT_DIR}/stats/pattern_summary.txt", "w") as f:
        f.write("SYNTACTIC PATTERN DETECTION SUMMARY\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total messages analyzed: {len(pat_df)}\n")
        f.write(f"With location pattern: {pat_df['has_location'].sum()} ({round(pat_df['has_location'].mean()*100,1)}%)\n")
        f.write(f"With action pattern: {pat_df['has_action'].sum()} ({round(pat_df['has_action'].mean()*100,1)}%)\n\n")
        f.write("Location pattern breakdown:\n")
        loc_counts = {}
        for row in pat_df["location_patterns"].dropna():
            for p in row.split("|"):
                if p:
                    loc_counts[p] = loc_counts.get(p, 0) + 1
        for k, v in sorted(loc_counts.items(), key=lambda x: -x[1]):
            f.write(f"  {k}: {v}\n")
        f.write("\nAction pattern breakdown:\n")
        act_counts = {}
        for row in pat_df["action_patterns"].dropna():
            for p in row.split("|"):
                if p:
                    act_counts[p] = act_counts.get(p, 0) + 1
        for k, v in sorted(act_counts.items(), key=lambda x: -x[1]):
            f.write(f"  {k}: {v}\n")

    # ── Save figures as CSV (chart-ready data) ────────────────────────────────
    pd.DataFrame(list(analysis["urgency_distribution"].items()),
                 columns=["level","count"]).to_csv(f"{OUTPUT_DIR}/figures/urgency.csv", index=False)

    pd.DataFrame(list(analysis["top_actions"].items()),
                 columns=["action","count"]).to_csv(f"{OUTPUT_DIR}/figures/actions.csv", index=False)

    pd.DataFrame(list(analysis["disaster_type_distribution"].items()),
                 columns=["type","count"]).to_csv(f"{OUTPUT_DIR}/figures/disaster_types.csv", index=False)

    pd.DataFrame(list(analysis["pos_high_urgency"].items()),
                 columns=["pos","ratio"]).head(10).to_csv(f"{OUTPUT_DIR}/figures/pos_high_urgency.csv", index=False)

    pd.DataFrame(list(analysis["pos_low_urgency"].items()),
                 columns=["pos","ratio"]).head(10).to_csv(f"{OUTPUT_DIR}/figures/pos_low_urgency.csv", index=False)

    print("✔ output/stats/ — 5 summary text files")
    print("✔ output/figures/ — 5 chart-ready CSV files")
    print("✔ All outputs saved!")

if __name__ == "__main__":
    main()