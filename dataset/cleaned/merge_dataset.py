import pandas as pd
from pathlib import Path

# ==========================================================
# CONFIGURATION
# ==========================================================

CLEAN_DIR = Path("dataset/cleaned")
OUTPUT_DIR = Path("dataset/final")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "merged_dataset.csv"

# ==========================================================
# LOAD DATASETS
# ==========================================================

csv_files = sorted(CLEAN_DIR.glob("*_clean.csv"))

datasets = []

print("=" * 80)
print("MERGING DATASETS")
print("=" * 80)

for file in csv_files:

    print(f"Loading: {file.name}")

    df = pd.read_csv(file)

    print(f"Rows: {len(df)}")

    datasets.append(df)

# ==========================================================
# MERGE
# ==========================================================

merged = pd.concat(datasets, ignore_index=True)

print("\nTotal rows before deduplication :", len(merged))

# ==========================================================
# REMOVE DUPLICATE TEXT
# ==========================================================

merged = merged.drop_duplicates(subset=["text"])

print("Total rows after deduplication  :", len(merged))

# ==========================================================
# RESET IDS
# ==========================================================

merged = merged.reset_index(drop=True)

merged["id"] = range(1, len(merged) + 1)

# ==========================================================
# SHUFFLE DATASET
# ==========================================================

merged = merged.sample(frac=1, random_state=42).reset_index(drop=True)

merged["id"] = range(1, len(merged) + 1)

# ==========================================================
# SAVE
# ==========================================================

merged.to_csv(OUTPUT_FILE, index=False)

# ==========================================================
# SUMMARY
# ==========================================================

print("\n" + "=" * 80)
print("MERGE SUMMARY")
print("=" * 80)

print(f"Final Dataset Size : {len(merged)}")

print("\nLabel Distribution")

print(merged["label"].value_counts())

print("\nAttack Types")

print(merged["attack_type"].value_counts())

print("\nObfuscation Types")

print(merged["obfuscation_type"].value_counts())

print("\nSource")

print(merged["source"].value_counts())

print("\nSaved to:")

print(OUTPUT_FILE)

print("\nDone.")