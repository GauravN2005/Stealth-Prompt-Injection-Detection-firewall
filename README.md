# Shield — AI-Driven Stealth Prompt Injection Detection Firewall

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2019-61DAFB.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

> **Submission for CODENIXIA AI/ML Industry Internship Technical Selection Challenge – 2026**

**Shield** is an enterprise-grade AI security firewall designed to detect invisible, obfuscated, and stealth prompt injection payloads hidden inside PDF, HTML, and text documents. By combining multi-layer document parsing, deterministic obfuscation uncloaking, and a fine-tuned **DistilBERT** sequence classifier, Shield inspects documents before they reach LLM processing pipelines, neutralizing prompt injection vectors at the perimeter.

---

## Table of Contents
- [1. Problem Statement](#1-problem-statement)
- [2. Target Users](#2-target-users)
- [3. Why AI/ML is Required](#3-why-aiml-is-required)
- [4. Proposed Solution](#4-proposed-solution)
- [5. Key Features](#5-key-features)
- [6. System Architecture](#6-system-architecture)
- [7. End-to-End Workflow](#7-end-to-end-workflow)
- [8. Technology Stack](#8-technology-stack)
- [9. Data & Model Documentation](#9-data--model-documentation)
- [10. Exploratory Data Analysis (EDA) Summary](#10-exploratory-data-analysis-eda-summary)
- [11. Architectural Justification: Why RAG is Not Used](#11-architectural-justification-why-rag-is-not-used)
- [12. Architectural Justification: Why an AI Agent is Not Used](#12-architectural-justification-why-an-ai-agent-is-not-used)
- [13. API Documentation](#13-api-documentation)
- [14. Error Handling & Observability](#14-error-handling--observability)
- [15. Installation & Setup](#15-installation--setup)
- [16. Docker Deployment](#16-docker-deployment)
- [17. Testing & Verification](#17-testing--verification)
- [18. CODENIXIA Assessment Alignment Matrix](#18-codenixia-assessment-alignment-matrix)

---

## 1. Problem Statement

As Retrieval-Augmented Generation (RAG) systems, document processing LLMs, and autonomous agents process untrusted user documents (PDFs, HTML web pages, Markdown), they become vulnerable to **Indirect Prompt Injection Attacks**. 

Attackers embed adversarial instructions designed to hijack the LLM's control flow, force credential exfiltration, or bypass safety system prompts. Crucially, modern prompt injection attacks use **stealth techniques** to remain completely invisible to human reviewers while being processed by document parsing pipelines:
- **Invisible PDF Text**: Text rendered with white font color (`RGB=(255,255,255)`) or microscopic font size ($\le 1.5\text{pt}$).
- **Document Metadata**: Malicious instructions placed inside PDF header attributes (`/Author`, `/Subject`, `/Title`).
- **Hidden CSS Elements**: Text styled with `display:none`, `visibility:hidden`, `opacity:0`, or `color:transparent`.
- **HTML Comments & Meta Attributes**: Instructions hidden inside `<!-- comments -->`, `<meta>` tags, or image `alt` text.
- **Unicode Obfuscation**: Zero-width invisible spaces (`\u200B`, `\uFEFF`, `\u200C`) or Cyrillic/Greek homoglyph character substitution (`а` $\rightarrow$ `a`).
- **Encoded Payloads**: Base64, Hexadecimal, and URL-encoded instructions uncloaked during processing.

Standard rule-based string matching fails to detect semantic variations of these payloads, while passing raw document text to an LLM exposes the guardrail itself to recursive prompt injection. Shield resolves this dilemma.

---

## 2. Target Users
- **AI Application Developers**: Teams integrating document upload features into LLM applications.
- **AI Security Engineers**: Security professionals establishing perimeter firewalls around enterprise RAG pipelines.
- **Enterprise DevSecOps Teams**: Organizations processing untrusted external PDF/HTML content at scale.

---

## 3. Why AI/ML is Required

1. **Semantic Generalization**: Prompt injections do not rely on fixed keywords. Attackers rephrase instructions using diverse vocabulary, roleplay tactics, and multi-lingual phrasing. A machine learning sequence classifier captures abstract semantic intent (`Safe` vs `Injection`) beyond fixed regular expressions.
2. **Hybrid Preprocessing Efficiency**: Pure ML models fail on raw obfuscated strings because tokenizers break zero-width spaces or Base64 hashes into meaningless tokens. Shield pairs **deterministic preprocessing** (uncloaking payloads) with **statistical ML classification** (evaluating uncloaked semantics).

---

## 4. Proposed Solution

Shield implements a two-stage security firewall:
1. **Deterministic Document Parsing & Uncloaking**: Extracts hidden document layers (PDF white text, HTML CSS hidden elements, metadata) and decodes zero-width unicode, homoglyphs, and Base64/Hex strings.
2. **Fine-Tuned DistilBERT Inference**: Passes each extracted text segment through a fine-tuned DistilBERT model to compute exact injection probability logit scores and risk ratings (`High`, `Medium`, `Low`).

---

## 5. Key Features

- **Multi-Format Document Extractor**: Parsing engine for `.pdf`, `.html`, `.txt`, and `.md` files (`extractors.py`).
- **Stealth Obfuscation Decoder**: Zero-width unicode stripper, Cyrillic/Greek homoglyph normalizer, and Base64/Hex/URL payload uncloaker (`obfuscation.py`).
- **Fine-Tuned Intelligence Layer**: DistilBERT sequence classifier trained on 72,418 security samples (`predict.py`).
- **Per-Segment Risk Aggregation**: Segment inspector identifying exact payload locations and risk severity hierarchy.
- **FastAPI Perimeter REST API**: Fully documented API with CORS, structured logging, and health checking (`app.py`).
- **React 19 Dashboard**: Real-time interactive UI with drag-and-drop file upload, warning indicators, and payload breakdown.

---

## 6. System Architecture

```
                                  USER / CLIENT
                 (React + Vite Dashboard / External API Consumers)
                                        │
                                        ▼
                             FASTAPI BACKEND ROUTER
           (app.py / CORS Middleware / Structured Logging / Health Check)
               │                        │                        │
               ▼                        ▼                        ▼
        [ GET /health ]        [ POST /scan-text ]      [ POST /scan-file ]
               │                        │                        │
               ▼                        v                        v
      +-----------------+      +-----------------+      +-----------------+
      | System Readiness|      | Raw Text Input  |      | PDF / HTML / TXT|
      +-----------------+      +-----------------+      +-----------------+
                                        │                        │
                                        │                        v
                                        │               +-----------------+
                                        │               | Layer Extractor |
                                        │               |  - PDF Metadata |
                                        │               |  - White Text   |
                                        │               |  - Micro Font   |
                                        │               |  - Hidden CSS   |
                                        │               |  - HTML Comments|
                                        │               +-----------------+
                                        │                        │
                                        +----------┬-------------+
                                                   │
                                                   v
                                  +---------------------------------+
                                  | Obfuscation Decoding Engine     |
                                  |  - Zero-width character stripper|
                                  |  - Homoglyph normalization      |
                                  |  - Base64 / Hex payload decoder |
                                  +---------------------------------+
                                                   │
                                                   v
                                  +---------------------------------+
                                  | Intelligence Layer              |
                                  | Fine-Tuned DistilBERT Model     |
                                  |  - 256 Max Token Sequence       |
                                  |  - Logit Softmax Probabilities  |
                                  |  - Stealth Layer Heuristics     |
                                  +---------------------------------+
                                                   │
                                                   v
                                  +---------------------------------+
                                  | Threat Aggregator & JSON Report |
                                  +---------------------------------+
```

---

## 7. End-to-End Workflow

```
Input Ingestion ➔ Document Extraction ➔ Obfuscation Uncloaking ➔ Segment Classification ➔ Threat Aggregation ➔ API JSON Output
```

1. **Ingestion**: Uploaded document or raw text prompt arrives at FastAPI endpoints.
2. **Extraction**: `extractors.py` separates visible body text from hidden document layers.
3. **Uncloaking**: `obfuscation.py` cleans invisible unicode, converts homoglyphs, and decodes Base64/Hex strings.
4. **Classification**: `predict.py` passes segments through DistilBERT, calculating probabilities.
5. **Aggregation**: Aggregates overall label (`Safe` vs `Injection`), max confidence score, and segment inspector details.

---

## 8. Technology Stack

| Layer | Technology | Selection Rationale |
|---|---|---|
| **ML Intelligence** | `DistilBERT` (`distilbert-base-uncased`) | Low inference latency (~15ms on CPU), small memory footprint (~267MB), deterministic output |
| **Backend Framework** | `FastAPI` 0.116 / `Uvicorn` 0.35 | Async I/O for file uploads, OpenAPI auto-generation, high performance |
| **PDF Extraction** | `pdfplumber` 0.11 / `pypdf` 5.3 | Font layout inspection, color coordinate filtering, metadata extraction |
| **HTML Extraction** | `BeautifulSoup4` 4.13 | DOM selector parsing for hidden CSS (`display:none`), comments, `<meta>` tags |
| **Frontend UI** | `React` 19 / `Vite` 6 / `Tailwind CSS` v4 | Fast HMR, responsive dark-mode security dashboard, modular components |
| **Testing** | `Pytest` 9.1 / `Starlette TestClient` | Automated unit, extraction, and API integration testing |
| **Containerization** | `Docker` / `Docker Compose` | Reproducible deployment with multi-stage build and HEALTHCHECK |

---

## 9. Data & Model Documentation

### Dataset Strategy
- **Total Samples**: 72,418 prompt samples
- **Source**: Merged prompt injection benchmarks (Pishield dataset, benign instruction sets)
- **Class Distribution**: 67,424 Injection prompts ($93.1\%$), 4,994 Safe prompts ($6.9\%$)
- **Train / Validation / Test Split**: $70\%$ Training (50,692), $15\%$ Validation (10,863), $15\%$ Testing (10,863)

### DistilBERT Fine-Tuning Setup (`Train_DistilBERT.ipynb`)
- **Base Architecture**: `distilbert-base-uncased` (6 transformer layers, 66M parameters)
- **Max Token Length**: 256 tokens
- **Optimizer**: AdamW ($\text{lr} = 2\times 10^{-5}$, weight decay = 0.01)
- **Batch Size**: 32 (Training), 64 (Evaluation)
- **Epochs**: 2

### Evaluation Results (Held-Out Test Set)
- **Evaluation Loss**: $3.107 \times 10^{-5}$
- **Test Accuracy**: $100.0\%$ ($99.98\%$)
- **Precision / Recall / F1-Score**: 1.00 / 1.00 / 1.00

### Model Limitations & Real-World Considerations
- **Dataset Imbalance**: Dataset contains high proportion of injection samples ($93\%$). In production, benign traffic dominates.
- **Obfuscation Shift**: Novel encoding schemes (e.g. custom ciphers) require updated preprocessors.
- **Length Truncation**: Inputs exceeding 256 tokens are segmented; extremely long documents depend on accurate segment splitting.

---

## 10. Exploratory Data Analysis (EDA) Summary

Analysis from `EDA_(RVU).ipynb` identified key structural patterns in prompt injection payloads:
1. **Word Count & Character Distributions**: Injection prompts exhibit higher average word counts ($\mu = 64$ words) compared to standard benign prompts ($\mu = 22$ words).
2. **Top Lexical Indicators**: Frequent injection tokens include `"ignore"`, `"system"`, `"prompt"`, `"instructions"`, `"bypass"`, and `"developer"`.
3. **Sequence Length**: 98.4% of all prompts fit within a 256-token context window, validating the choice of 256 max sequence length for DistilBERT efficiency.

---

## 11. Architectural Justification: Why RAG is Not Used

**RAG (Retrieval-Augmented Generation) was explicitly omitted from the Shield core pipeline.**

- **Functional Scope**: Shield's objective is real-time binary sequence classification (`Safe` vs `Injection`) and document layer uncloaking. It is a security perimeter firewall, not a question-answering system.
- **Latency Constraints**: Vector database retrieval ($>200\text{ms}$) introduces unnecessary execution bottlenecks into inline API firewall inspection.
- **Architectural Simplicity**: A fine-tuned sequence classifier operating on uncloaked text provides deterministic, low-latency scoring without vector database maintenance overhead.

---

## 12. Architectural Justification: Why an AI Agent is Not Used

**Autonomous AI Agent frameworks (e.g., LangChain/LangGraph agent loops) were explicitly omitted.**

- **Deterministic Security**: Security firewalls must follow deterministic $O(1)$ routing rules ($A \rightarrow B \rightarrow C$). Agent loops introduce non-deterministic tool selection and execution delays.
- **Hijacking Immunity**: Allowing an AI agent to execute dynamic tools while processing adversarial prompt injection payloads creates a vulnerability where the agent itself can be hijacked by indirect injection.

---

## 13. API Documentation

### Base URL: `http://127.0.0.1:8000`

#### 1. Service Root `GET /`
- **Purpose**: Returns service metadata and active security features.
- **Response**: `200 OK`

#### 2. Health Check `GET /health`
- **Purpose**: Returns health status, model readiness, and timestamp.
- **Response**:
  ```json
  {
    "status": "healthy",
    "model_loaded": true,
    "model_architecture": "DistilBertForSequenceClassification",
    "version": "2.0",
    "timestamp": "2026-08-15T22:30:00Z"
  }
  ```

#### 3. Legacy Text Scan `POST /predict`
- **Input**: `{"text": "string"}`
- **Response**: `{"label": "Safe" | "Injection", "confidence": float, "risk_level": "High" | "Medium" | "Low", "processing_time_ms": float}`

#### 4. Stealth Text Scan `POST /scan-text`
- **Input**: `{"text": "string"}`
- **Purpose**: Analyzes text for zero-width characters, homoglyphs, and embedded Base64/Hex strings before classification.

#### 5. Stealth File Scan `POST /scan-file`
- **Input**: `multipart/form-data` with `file` upload (`.pdf`, `.html`, `.txt`, `.md`).
- **Response Example**:
  ```json
  {
    "overall_label": "Injection",
    "confidence": 99.46,
    "risk_level": "High",
    "processing_time_ms": 42.15,
    "filename": "document.pdf",
    "file_size_bytes": 10485,
    "obfuscation_warnings": [
      "[PDF Page 1 (White-on-White Layer)] Zero-width unicode stealth detected: 2 Zero-Width Space(s)"
    ],
    "segments": [
      {
        "source": "PDF Page 1 (White-on-White Layer)",
        "text_snippet": "Ignore previous instructions...",
        "is_hidden": true,
        "reason": "Invisible text color matching white background",
        "label": "Injection",
        "confidence": 99.46,
        "risk_level": "High"
      }
    ]
  }
  ```

---

## 14. Error Handling & Observability

- **Structured Logging**: Uses standard Python `logging` module (`shield.api`) recording request events, file types, segment counts, and execution metrics.
- **Sanitized Exception Handling**: Returns HTTP 400 for empty payloads, unsupported formats (`.exe`, `.bin`), and HTTP 500 for parsing errors without exposing internal stack traces.

---

## 15. Installation & Setup

### Prerequisites
- Python 3.10 or 3.11
- Node.js 18+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/GauravN2005/Stealth-Prompt-Injection-Detection-firewall.git
cd Stealth-Prompt-Injection-Detection-firewall
```

### 2. Environment & Model Download
```bash
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate      # On Windows
# source .venv/bin/activate   # On Linux/macOS

# Install backend dependencies
pip install -r backend/requirements.txt

# Download fine-tuned DistilBERT weights (~267 MB from Hugging Face Hub)
python setup_model.py
```

### 3. Start Backend API
```bash
cd backend
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```
*API docs available at:* `http://127.0.0.1:8000/docs`

### 4. Start Frontend Dashboard
```bash
cd frontend
npm install
npm run dev
```
*Dashboard available at:* `http://localhost:5173`

---

## 16. Docker Deployment

### Build Container Image
```bash
docker build -t shield-firewall .
```

### Run Container
```bash
docker run -d -p 8000:8000 --name shield-container shield-firewall
```

### Test Container Health
```bash
curl http://localhost:8000/health
```

---

## 17. Testing & Verification

### Automated Pytest Suite
Run the 9-test integration suite covering root, health, text scan, file upload, and error handling:
```bash
python -m pytest tests/test_api.py
```

### Standalone Stealth Engine Test
```bash
python backend/test_stealth.py
```

---

## 18. CODENIXIA Assessment Alignment Matrix

| Milestone | Requirement | Shield Implementation Status | Project Component |
|---|---|---|---|
| **1** | Problem Discovery & Solution Design | ✅ Complete | Problem statement, target users, multi-layer stealth detection design (`README.md`) |
| **2** | Data & Knowledge Strategy | ✅ Complete | 72,418 sample dataset strategy, 70/15/15 train-val-test split (`Train_DistilBERT.ipynb`) |
| **3** | Python Data-Processing Pipeline | ✅ Complete | Document layer extractors (`extractors.py`), obfuscation decoder (`obfuscation.py`) |
| **4** | Data Analysis & ML Fundamentals | ✅ Complete | EDA notebook (`EDA_(RVU).ipynb`), word counts, token analysis, lexical charts |
| **5** | ML/LLM Intelligence Layer | ✅ Complete | Fine-tuned DistilBERT sequence classifier (`predict.py`, `model.py`) |
| **6** | RAG Architecture | ✅ Complete (Justified Omission) | Technical rationale explaining why RAG is inappropriate for binary security firewall (`README.md`, `DECISION_LOG.md`) |
| **7** | AI Agent Architecture | ✅ Complete (Justified Omission) | Technical rationale explaining why non-deterministic agents present security risks (`README.md`, `DECISION_LOG.md`) |
| **8** | Application & API | ✅ Complete | FastAPI REST API (`app.py`), React 19 interactive security dashboard (`frontend/`) |
| **9** | Containerization & Infrastructure | ✅ Complete | Multi-stage `Dockerfile`, `.dockerignore`, `.env.example`, automated model downloader (`setup_model.py`) |
| **10** | Testing, Observability & Readiness | ✅ Complete | Pytest suite (`tests/test_api.py`), logging (`app.py`), `DEBUGGING_REPORT.md`, `AI_USAGE.md` |

---

## License
Developed for academic submission and assessment.
