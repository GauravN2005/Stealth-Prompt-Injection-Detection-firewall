from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = str(BASE_DIR / "prompt_injection_detector")

print("Loading tokenizer...")
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)

print("Loading model...")
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

print("Model loaded successfully!")