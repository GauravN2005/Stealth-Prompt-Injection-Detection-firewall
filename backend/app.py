import logging
import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from predict import predict_prompt, predict_stealth_scan
from extractors import extract_pdf_layers, extract_html_layers, extract_text_layers
from obfuscation import analyze_obfuscation
from model import model, tokenizer

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("shield.api")

app = FastAPI(
    title="Shield // AI Prompt Injection & Stealth Payload Detector API",
    description="Firewall API that detects obfuscated and stealth prompt injections hidden inside PDF, HTML, and text documents.",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    text: str


@app.get("/")
def home():
    """Root endpoint detailing API info and key security features."""
    return {
        "service": "Shield Prompt Injection Firewall",
        "status": "online",
        "version": "2.0",
        "features": [
            "DistilBERT sequence classification",
            "PDF white-text and microscopic font stealth detection",
            "HTML hidden CSS, metadata, and comment layer parsing",
            "Zero-width unicode anomaly stripping",
            "Base64, Hex, and URL payload uncloaking"
        ]
    }


@app.get("/health")
def health_check():
    """Health check endpoint evaluating model status and API readiness."""
    model_loaded = model is not None and tokenizer is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "model_architecture": "DistilBertForSequenceClassification",
        "version": "2.0",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }


@app.post("/predict")
def predict(request: PromptRequest):
    """Legacy single text prompt prediction endpoint."""
    logger.info("Received request on /predict endpoint")
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Empty prompt provided.")
    try:
        return predict_prompt(request.text)
    except Exception as e:
        logger.error(f"Error in /predict: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction pipeline failure.")


@app.post("/scan-text")
def scan_text(request: PromptRequest):
    """
    Enhanced text scanner that analyzes raw text for zero-width characters,
    homoglyphs, and embedded Base64/Hex encodings before classification.
    """
    text = request.text.strip() if request.text else ""
    if not text:
        raise HTTPException(status_code=400, detail="Empty text prompt provided.")

    logger.info(f"Scanning text prompt of length {len(text)}")
    try:
        obf_result = analyze_obfuscation(text)
        
        has_obfuscation = obf_result["zero_width_count"] > 0 or obf_result["homoglyph_count"] > 0

        # Primary cleaned text segment
        segments = [{
            "source": "Primary Text Prompt",
            "text": obf_result["cleaned_text"],
            "is_hidden": has_obfuscation,
            "reason": "Stealth obfuscation detected (Zero-width / Homoglyph characters)" if has_obfuscation else None
        }]

        # Add any decoded payloads found
        segments.extend(obf_result["decoded_segments"])

        report = predict_stealth_scan(segments, obf_result["warnings"])
        logger.info(f"Text scan completed. Risk: {report.get('risk_level')}, Overall: {report.get('overall_label')}")
        return report
    except Exception as e:
        logger.error(f"Error in /scan-text: {str(e)}")
        raise HTTPException(status_code=500, detail="Text scan analysis failed.")


@app.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    """
    Scans uploaded PDF, HTML, or TXT documents for stealth prompt injections,
    extracting visible body text, invisible white-on-white text, hidden CSS elements,
    HTML comments, metadata, and uncloaked payloads.
    """
    filename = file.filename or "uploaded_file"
    logger.info(f"Scanning uploaded file: '{filename}'")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    extracted_segments = []
    filename_lower = filename.lower()

    try:
        if filename_lower.endswith(".pdf"):
            extracted_segments = extract_pdf_layers(file_bytes)
        elif filename_lower.endswith((".html", ".htm")):
            html_content = file_bytes.decode("utf-8", errors="ignore")
            extracted_segments = extract_html_layers(html_content)
        elif filename_lower.endswith((".txt", ".md", ".json", ".log", ".csv")):
            text_content = file_bytes.decode("utf-8", errors="ignore")
            extracted_segments = extract_text_layers(text_content)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{filename}'. Allowed formats: PDF, HTML, TXT, MD."
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to extract layers from '{filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse document: {str(e)}")

    if not extracted_segments:
        raise HTTPException(status_code=400, detail="Could not extract readable text segments from the file.")

    try:
        # Process all segments through obfuscation analyzer
        all_segments = []
        all_warnings = []

        for seg in extracted_segments:
            seg_text = seg["text"]
            obf_res = analyze_obfuscation(seg_text)

            # Update segment text to cleaned text
            seg["text"] = obf_res["cleaned_text"]
            if obf_res["zero_width_count"] > 0 or obf_res["homoglyph_count"] > 0:
                seg["is_hidden"] = True
                seg["reason"] = seg.get("reason") or "Zero-width / Homoglyph stealth characters detected"
            all_segments.append(seg)

            # Collect warnings
            for w in obf_res["warnings"]:
                all_warnings.append(f"[{seg['source']}] {w}")

            # Add any decoded payloads found within this segment
            for dec_seg in obf_res["decoded_segments"]:
                all_segments.append({
                    "source": f"[{seg['source']}] {dec_seg['source']}",
                    "text": dec_seg["text"],
                    "is_hidden": True,
                    "reason": dec_seg["reason"]
                })

        report = predict_stealth_scan(all_segments, all_warnings)
        report["filename"] = filename
        report["file_size_bytes"] = len(file_bytes)
        logger.info(f"File scan complete for '{filename}'. Overall: {report.get('overall_label')}, Risk: {report.get('risk_level')}")
        return report
    except Exception as e:
        logger.error(f"Prediction failed for file '{filename}': {str(e)}")
        raise HTTPException(status_code=500, detail="Stealth scan processing failed.")