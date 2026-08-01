import pandas as pd

df = pd.read_csv("dataset/cleaned/pishield_clean.csv")

df["label"] = "Injection"

df.to_csv("dataset/cleaned/pishield_clean.csv", index=False)

print("PIShield labels corrected.")