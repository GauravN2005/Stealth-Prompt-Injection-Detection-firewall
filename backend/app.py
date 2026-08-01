from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from predict import predict_prompt, predict_stealth_scan
from extractors import extract_pdf_layers, extract_html_layers, extract_text_layers
from obfuscation import analyze_obfuscation

app = FastAPI(
    title="Shield // AI Prompt Injection & Stealth Payload Detector API",
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


@app.post("/predict")
def predict(request: PromptRequest):
    """Legacy single text prompt prediction endpoint."""
    return predict_prompt(request.text)


@app.post("/scan-text")
def scan_text(request: PromptRequest):
    """
    Enhanced text scanner that analyzes raw text for zero-width characters,
    homoglyphs, and embedded Base64/Hex encodings before classification.
    """
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty text prompt provided.")

    obf_result = analyze_obfuscation(text)
    
    # Primary cleaned text segment
    segments = [{
        "source": "Primary Text Prompt",
        "text": obf_result["cleaned_text"],
        "is_hidden": False,
        "reason": None
    }]

    # Add any decoded payloads found
    segments.extend(obf_result["decoded_segments"])

    return predict_stealth_scan(segments, obf_result["warnings"])


@app.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    """
    Scans uploaded PDF, HTML, or TXT documents for stealth prompt injections,
    extracting visible body text, invisible white-on-white text, hidden CSS elements,
    HTML comments, metadata, and uncloaked payloads.
    """
    filename = file.filename or "uploaded_file"
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
        else: # Plain text / Markdown
            text_content = file_bytes.decode("utf-8", errors="ignore")
            extracted_segments = extract_text_layers(text_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse document: {str(e)}")

    if not extracted_segments:
        raise HTTPException(status_code=400, detail="Could not extract readable text segments from the file.")

    # Process all segments through obfuscation analyzer
    all_segments = []
    all_warnings = []

    for seg in extracted_segments:
        seg_text = seg["text"]
        obf_res = analyze_obfuscation(seg_text)

        # Update segment text to cleaned text
        seg["text"] = obf_res["cleaned_text"]
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
    return report