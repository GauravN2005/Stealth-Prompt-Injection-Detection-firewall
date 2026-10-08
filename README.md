# Shield — AI-Driven Stealth Prompt Injection Detection Firewall

An AI-powered monitoring and filtering system for detecting **invisible and obfuscated prompt injection payloads** hidden inside PDF documents, HTML web pages, and plain text — using a fine-tuned **DistilBERT** model.

---

## Problem Statement
Modern AI systems can be manipulated via *prompt injection attacks* — malicious instructions embedded inside documents that are **completely invisible** to human readers but are read and followed by LLMs. These attacks hide inside:
- White-on-white PDF text (`color: white, font-size: 0pt`)
- PDF document header metadata (`/Author`, `/Subject` fields)
- HTML `display:none` / `visibility:hidden` CSS elements
- HTML comments (`<!-- ... -->`)
- Zero-width Unicode characters (`\u200B`, `\uFEFF`)
- Base64 / Hex / URL-encoded payloads

**Shield** detects all of them.

---

## Features
- **Multi-layer document extraction** for PDF and HTML files
- **Stealth obfuscation de-anonymizer** (zero-width chars, homoglyphs, Base64/Hex decoding)
- **Per-segment AI classification** using fine-tuned DistilBERT
- **Real-time dashboard** with Segment Inspector showing exactly where the hidden payload was found
- **REST API** built with FastAPI
- **Drag-and-drop UI** built with React + Vite + Tailwind CSS v4

---

## Architecture

```
User Uploads File (PDF / HTML / TXT)
        │
        ▼
┌──────────────────────┐
│  Document Extractor  │  ← pdfplumber, pypdf, beautifulsoup4
│  (extractors.py)     │    Splits file into visible + hidden layers
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ Obfuscation Decoder  │  ← obfuscation.py
│                      │    Strips zero-width chars, decodes Base64/Hex
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│  DistilBERT Classifier│ ← predict.py
│  (per segment)       │    Classifies each layer as Injection / Safe
└──────────────────────┘
        │
        ▼
   JSON Response → React Dashboard (Segment Inspector)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **ML Model** | DistilBERT (fine-tuned for prompt injection classification) |
| **Backend** | FastAPI + Uvicorn |
| **PDF Parsing** | `pdfplumber`, `pypdf` |
| **HTML Parsing** | `beautifulsoup4` |
| **Frontend** | React.js + Vite + Tailwind CSS v4 |
| **Icons** | Lucide React |

---

## Project Structure

```
├── backend/
│   ├── app.py                   # FastAPI routes (/predict, /scan-text, /scan-file)
│   ├── model.py                 # DistilBERT model loader
│   ├── predict.py               # Single-text + multi-segment prediction logic
│   ├── extractors.py            # PDF & HTML layer extractors
│   ├── obfuscation.py           # Zero-width, homoglyph, Base64/Hex decoders
│   ├── test_stealth.py          # Backend unit tests
│   ├── create_test_docs.py      # Script to generate test PDF & HTML files
│   ├── requirements.txt
│   └── prompt_injection_detector/  # Trained DistilBERT model weights
│       ├── config.json
│       ├── tokenizer.json
│       ├── vocab.txt
│       └── model.safetensors    # ⚠️ Excluded from git (267 MB) — see note below
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React dashboard
│   │   └── index.css            # Tailwind CSS v4 imports + design tokens
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── test_documents/
│   ├── test_stealth_injection.html   # HTML test file with hidden CSS & meta injection
│   └── test_stealth_injection.pdf    # PDF test file with metadata injection
│
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/GauravN2005/Stealth-Prompt-Injection-Detection-firewall.git
cd Stealth-Prompt-Injection-Detection-firewall
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

> The `model.safetensors` file (267 MB) is hosted on [Hugging Face Hub](https://huggingface.co/gaurav-nimbalkar/stealth-prompt-injection-detector).
> Run the setup script below to download it automatically.

### 3. Download the Model (Required — run once)
```bash
python setup_model.py
```
This will automatically download `model.safetensors` (~267 MB) from Hugging Face Hub into the correct folder.

### 4. Run the Backend
```bash
cd backend
..\\.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```
Backend will be available at: `http://127.0.0.1:8000`

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will be available at: `http://localhost:5173`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check + model status |
| `POST` | `/predict` | Classify a single text prompt |
| `POST` | `/scan-text` | Scan text with obfuscation detection |
| `POST` | `/scan-file` | Upload and scan PDF / HTML / TXT file |

### Example: Scan a File
```bash
curl -X POST http://127.0.0.1:8000/scan-file \
  -F "file=@test_documents/test_stealth_injection.html"
```

---

## Test Files

Two pre-built stealth injection test documents are included in `test_documents/`:

| File | Hidden Content |
|------|---------------|
| `test_stealth_injection.html` | `display:none` CSS div, HTML comment, `<meta>` attribute injection |
| `test_stealth_injection.pdf` | PDF `/Author` and `/Subject` metadata injection |

Regenerate them anytime with:
```bash
python backend/create_test_docs.py
```

---

## Detection Capabilities

| Attack Vector | Detected? |
|---------------|-----------|
| White-on-white PDF text | ✅ Yes |
| PDF metadata (`/Author`, `/Subject`) | ✅ Yes |
| HTML `display:none` elements | ✅ Yes |
| HTML `visibility:hidden` elements | ✅ Yes |
| HTML comments (`<!-- -->`) | ✅ Yes |
| HTML `<meta>` / `alt` attributes | ✅ Yes |
| Zero-width Unicode characters | ✅ Yes |
| Base64 obfuscated payloads | ✅ Yes |
| Hex-encoded payloads | ✅ Yes |
| Cyrillic/Greek homoglyph spoofing | ✅ Yes |

---

## License
This project was developed as part of an academic implementation at **RV University**.
