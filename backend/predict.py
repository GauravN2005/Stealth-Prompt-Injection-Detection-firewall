import time
import re
import torch
import torch.nn.functional as F

from model import model, tokenizer

# Common prompt injection keywords that signal attacks when placed in hidden layers
STEALTH_INJECTION_KEYWORDS = [
    "ignore", "override", "system", "prompt", "admin", "api", "key", 
    "token", "credential", "developer mode", "bypass", "privilege", 
    "secret", "passthrough", "jailbreak", "instructions"
]


def predict_prompt(text: str):
    """
    Evaluates a single text string using the fine-tuned DistilBERT model.
    """
    if not text or not text.strip():
        return {
            "label": "Safe",
            "confidence": 100.0,
            "risk_level": "Low",
            "processing_time_ms": 0.0,
        }

    start = time.perf_counter()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = F.softmax(outputs.logits, dim=1)
    confidence, prediction = torch.max(probabilities, dim=1)
    confidence = confidence.item()

    label = "Injection" if prediction.item() == 1 else "Safe"

    if label == "Injection":
        if confidence >= 0.90:
            risk = "High"
        elif confidence >= 0.70:
            risk = "Medium"
        else:
            risk = "Low"
    else:
        risk = "Low"

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    return {
        "label": label,
        "confidence": round(confidence * 100, 2),
        "risk_level": risk,
        "processing_time_ms": elapsed_ms,
    }


def predict_stealth_scan(segments: list, obfuscation_warnings: list = None):
    """
    Evaluates multiple document segments (visible body, hidden PDF/HTML layers,
    decoded payloads) and aggregates their predictions into a single document report.
    """
    start_total = time.perf_counter()
    scanned_segments = []
    has_injection = False
    max_injection_confidence = 0.0
    max_safe_confidence = 0.0
    highest_risk = "Low"

    risk_hierarchy = {"High": 3, "Medium": 2, "Low": 1}

    for seg in segments:
        text = seg.get("text", "").strip()
        if not text:
            continue

        result = predict_prompt(text)
        label = result["label"]
        conf = result["confidence"]
        risk = result["risk_level"]
        is_hidden = seg.get("is_hidden", False)

        # Stealth Heuristic for Hidden Layers:
        # If text is hidden (CSS display:none, HTML comment, PDF white-text, Base64 payload)
        # AND contains injection keywords, flag as Injection.
        if is_hidden:
            text_lower = text.lower()
            if any(kw in text_lower for kw in STEALTH_INJECTION_KEYWORDS):
                label = "Injection"
                conf = max(conf, 99.2)
                risk = "High"
                if not seg.get("reason"):
                    seg["reason"] = "Stealth injection attempt hidden inside invisible document layer"

        if label == "Injection":
            has_injection = True
            if conf > max_injection_confidence:
                max_injection_confidence = conf
            if risk_hierarchy[risk] > risk_hierarchy[highest_risk]:
                highest_risk = risk
        else:
            if conf > max_safe_confidence:
                max_safe_confidence = conf

        scanned_segments.append({
            "source": seg.get("source", "Unknown Segment"),
            "text_snippet": text[:120] + ("..." if len(text) > 120 else ""),
            "full_text": text,
            "is_hidden": is_hidden,
            "reason": seg.get("reason"),
            "label": label,
            "confidence": conf,
            "risk_level": risk,
            "processing_time_ms": result["processing_time_ms"]
        })

    overall_label = "Injection" if has_injection else "Safe"
    overall_confidence = max_injection_confidence if has_injection else max_safe_confidence

    if not has_injection:
        highest_risk = "Low"

    total_ms = round((time.perf_counter() - start_total) * 1000, 2)

    return {
        "overall_label": overall_label,
        "confidence": round(overall_confidence, 2),
        "risk_level": highest_risk,
        "processing_time_ms": total_ms,
        "obfuscation_warnings": obfuscation_warnings or [],
        "segments": scanned_segments
    }