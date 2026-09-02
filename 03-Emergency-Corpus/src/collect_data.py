import pandas as pd
import os
from datasets import load_dataset

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

def fetch_humaid():
    print("\n[1/2] Fetching QCRI/HumAID-all via direct parquet download...")
    import io, requests
    dfs = []
    files = {
        "train": "https://huggingface.co/datasets/QCRI/HumAID-all/resolve/refs%2Fconvert%2Fparquet/default/train/0000.parquet",
        "validation": "https://huggingface.co/datasets/QCRI/HumAID-all/resolve/refs%2Fconvert%2Fparquet/default/validation/0000.parquet",
        "test": "https://huggingface.co/datasets/QCRI/HumAID-all/resolve/refs%2Fconvert%2Fparquet/default/test/0000.parquet",
    }
    for split, url in files.items():
        try:
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            df = pd.read_parquet(io.BytesIO(r.content))
            df["split"] = split
            df["source"] = "HumAID"
            dfs.append(df)
            print(f"  ✔ {split}: {len(df)} rows, columns: {list(df.columns)}")
        except Exception as e:
            print(f"  ✘ {split} failed: {e}")
    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        combined.to_csv(f"{RAW_DIR}/humaid_raw.csv", index=False)
        print(f"  ✔ HumAID total: {len(combined)} messages saved.")
        return combined
    return pd.DataFrame()

def create_manual_samples():
    print("\n[2/2] Creating manual Indian-context emergency samples...")
    samples = [
        {"tweet_text": "Massive earthquake hit Kathmandu, buildings collapsed near Durbar Square, need rescue teams immediately!", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "SOS! Trapped under rubble at MG Road Bangalore after earthquake. Send help now!", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "Flood water rising rapidly in Dharavi Mumbai. Families stranded on rooftops. Need boats!", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "Highway 44 completely submerged near Nagpur. Vehicles stranded. Emergency services needed.", "class_label": "infrastructure_and_utility_damage"},
        {"tweet_text": "Please send relief to Patna district. Entire village underwater. No food or medicine.", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "Forest fire spreading toward residential area in Shimla Hills. Evacuate sector 4 now!", "class_label": "caution_and_advice"},
        {"tweet_text": "Cyclone Amphan hitting West Bengal coast. People in South 24 Parganas must evacuate now.", "class_label": "caution_and_advice"},
        {"tweet_text": "Tsunami warning issued for Tamil Nadu coast. Evacuate Chennai Marina beach area immediately!", "class_label": "caution_and_advice"},
        {"tweet_text": "Mass casualty at Rajiv Chowk metro Delhi. Need doctors and ambulances at platform 3.", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "Bridge collapsed on Godavari river near Rajahmundry. Many vehicles fell. SOS!", "class_label": "infrastructure_and_utility_damage"},
        {"tweet_text": "Landslide blocked Manali-Leh highway. 3 buses stuck with passengers. Need helicopters.", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "pls help flod in our area nd no1 is cmng 2 help us we r stuck", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "URGENT SOS earthquake destroyed our house family trapped send help asap location: sector 7 rohini", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "helppp!! fire in bilding near mg road cant get out smoke evrywr call 100", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "Gas pipeline explosion near Vijayawada. People in 2km radius please evacuate.", "class_label": "caution_and_advice"},
        {"tweet_text": "Train derailed near Balasore Odisha. Multiple coaches off track. Emergency medical help needed now.", "class_label": "injured_or_dead_people"},
        {"tweet_text": "Mine collapse in Dhanbad Jharkhand. 15 workers trapped 200 feet underground. NDRF needed.", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "Chemical leak at Bhopal industrial zone. Workers unconscious. Send hazmat and medical teams.", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "District Collector Raigad announces mandatory evacuation of all coastal villages within 5km of shoreline.", "class_label": "displaced_people_and_evacuations"},
        {"tweet_text": "NDRF teams deployed to flood-affected areas of Sangli district. Relief operations underway.", "class_label": "rescue_volunteering_or_donation_effort"},
        {"tweet_text": "IMD issues red alert for heavy rainfall in Himachal Pradesh. Landslide risk high near Kullu.", "class_label": "caution_and_advice"},
        {"tweet_text": "State government opens 150 relief camps across 12 flood-affected districts in Assam.", "class_label": "displaced_people_and_evacuations"},
        {"tweet_text": "Rescue operation continues at Chamoli disaster site. 30 workers still missing underground.", "class_label": "missing_or_found_people"},
        {"tweet_text": "Drought conditions critical in Marathwada. Villages have no water for 3 weeks. Need tankers.", "class_label": "requests_or_urgent_needs"},
        {"tweet_text": "Building fire at Karol Bagh Delhi. People trapped on upper floors. Fire brigade not reachable.", "class_label": "requests_or_urgent_needs"},
    ]
    df = pd.DataFrame(samples)
    df["source"] = "manual"
    df["split"] = "manual"
    df.to_csv(f"{RAW_DIR}/manual_samples.csv", index=False)
    print(f"  ✔ Manual: {len(df)} messages saved.")
    return df

def main():
    print("=" * 60)
    print("  EMERGENCY CORPUS — DATA COLLECTION")
    print("=" * 60)

    dfs = []

    df1 = fetch_humaid()
    if not df1.empty:
        df1["source"] = "HumAID"
        dfs.append(df1)

    df2 = create_manual_samples()
    dfs.append(df2)

    print("\n[Combining all sources...]")
    combined = pd.concat(dfs, ignore_index=True)

    # Standardize to text / disaster_type columns
    combined = combined.rename(columns={"tweet_text": "text", "class_label": "disaster_type"})
    combined = combined[combined["text"].notna()]
    combined = combined[combined["text"].astype(str).str.strip() != ""]
    combined["disaster_type"] = combined["disaster_type"].fillna("unknown")
    combined["source"] = combined["source"].fillna("unknown")

    final = combined[["text", "disaster_type", "source"]].copy()
    final["text"] = final["text"].astype(str)
    final.reset_index(drop=True, inplace=True)
    final.index.name = "id"
    final.to_csv(f"{RAW_DIR}/all_raw.csv")

    print(f"\n✔ Combined corpus: {len(final)} messages")
    print(f"✔ Saved to: {RAW_DIR}/all_raw.csv")
    print("\nDisaster type distribution (top 15):")
    print(final["disaster_type"].value_counts().head(15).to_string())
    print("\nSource distribution:")
    print(final["source"].value_counts().to_string())
    print("\n✔ Data collection complete!")

if __name__ == "__main__":
    main()