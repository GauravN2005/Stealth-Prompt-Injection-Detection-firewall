import pandas as pd
import re
from pathlib import Path

# -----------------------------
# CONFIGURATION
# -----------------------------
RAW_DIR = Path("C:\\RV University Implemetation\\dataset\\raw")
OUTPUT_DIR = Path("C:\\RV University Implemetation\\dataset\\cleaned")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MIN_TEXT_LENGTH = 5

# -----------------------------
# Text Cleaning Function
# -----------------------------
def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # Remove leading/trailing spaces
    text = text.strip()

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove replacement characters
    text = text.replace("\ufffd", "")

    return text

# -----------------------------
# Clean One Dataset
# -----------------------------
def clean_dataset(file_path):

    print(f"\nProcessing: {file_path.name}")

    df = pd.read_csv(file_path)

    # Remove rows with missing text
    df = df.dropna(subset=["text"])

    # Clean text
    df["text"] = df["text"].apply(clean_text)

    # Remove empty strings
    df = df[df["text"] != ""]

    # Remove short prompts
    df = df[df["text"].str.len() >= MIN_TEXT_LENGTH]

    # Remove duplicate prompts
    df = df.drop_duplicates(subset=["text"])

    # Standardize labels
    if "label" in df.columns:
        df["label"] = df["label"].replace({
            "safe": "Safe",
            "SAFE": "Safe",
            "injection": "Injection",
            "attack": "Injection",
            "malicious": "Injection"
        })

    output_file = OUTPUT_DIR / file_path.name.replace(".csv", "_clean.csv")

    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file.name}")
    print(f"Rows: {len(df)}")

# -----------------------------
# Process All CSV Files
# -----------------------------
csv_files = list(RAW_DIR.glob("*.csv"))

for csv_file in csv_files:
    clean_dataset(csv_file)

print("\nDone!")