# AI Usage Disclosure — Shield Firewall

This document provides a transparent, comprehensive declaration of the AI tools utilized during the research, development, and submission preparation for **Shield — AI-Driven Stealth Prompt Injection Detection Firewall**.

---

## Summary of AI Tools Used

| Tool | Purpose | Type of Assistance | Human Review & Modifications |
|---|---|---|---|
| **Google DeepMind Antigravity / Gemini** | Architecture refinement, unit test generation, code auditing, documentation structuring | Code generation, test suite writing, technical writing | Handled all prompt engineering, reviewed line-by-line, executed test suite, verified model inference locally, customized regex parsers. |
| **ChatGPT / Claude (Anthropic)** | Initial dataset research & baseline DistilBERT hyperparameter recommendations | Conceptual guidance, training loop optimization strategies | Adapted Hugging Face Trainer arguments, tuned batch sizes (32), learning rate ($2\times 10^{-5}$), and evaluation metrics. |
| **GitHub Copilot** | Inline code autocompletion | Syntax autocompletion during document extractor implementation | Audited color threshold formulas, verified PyPDF metadata dictionary keys, updated CSS parser selectors. |

---

## Detailed Breakdown of Assistance

### 1. Document Extraction & Obfuscation Decoding Modules
- **AI Contribution**: Suggested regular expression patterns for Base64 payload detection (`[A-Za-z0-9+/]{12,}={0,2}`) and HTML BeautifulSoup selector logic for hidden style attributes (`display:none`, `opacity:0`, `visibility:hidden`, `color:transparent`).
- **Student Verification & Refinement**: Added fallback character set decoding (`latin-1`/`utf-8` ignore mode), implemented zero-width unicode character stripping table (`\u200B`, `\u200C`, `\u200D`, `\uFEFF`, `\u00AD`), and created white-on-white text RGB/CMYK color boundary checks in `pdfplumber`.

### 2. Model Training & Fine-Tuning Pipeline
- **AI Contribution**: Provided template code for Hugging Face `Trainer` and dataset tokenization using `DistilBertTokenizerFast`.
- **Student Verification & Refinement**: Verified dataset split ratios (70% train, 15% validation, 15% test on 72,418 samples), monitored training loss convergence across 2 epochs, and evaluated accuracy ($100.0\%$) and loss ($3.1\times 10^{-5}$) on test set.

### 3. API, Containerization & Engineering Readiness
- **AI Contribution**: Generated initial FastAPI endpoint skeletons (`app.py`), pytest suite template (`tests/test_api.py`), and multi-stage `Dockerfile`.
- **Student Verification & Refinement**: Added structured logging (`logging.getLogger("shield.api")`), created `/health` health-check endpoint, added strict HTTP exception handling (400 for empty/unsupported files, 500 for parsing errors), and verified container containerization setup.

---

## Human Engineering & Accountability Statement

The final implementation was thoroughly reviewed, modified, compiled, containerized, and tested by the student. All security boundaries, model inference pipelines, extractor logic, and assessment documentation have been validated using concrete automated tests (`python backend/test_stealth.py` and `pytest tests/test_api.py`). No AI tool generated unverified code or fabricated metrics.
