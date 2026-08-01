import pandas as pd

df = pd.read_csv("dataset/final/merged_dataset.csv")

df["attack_type"] = df["attack_type"].fillna("Prompt Injection")
df["obfuscation_type"] = df["obfuscation_type"].fillna("None")

df.to_csv("dataset/final/merged_dataset.csv", index=False)

print("Metadata updated successfully.")