# System Architecture — Shield Firewall

This directory contains technical diagrams and flow specifications for **Shield — AI-Driven Stealth Prompt Injection Detection Firewall**.

---

## High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                 USER / CLIENT                                     |
|               (React + Vite Dashboard / External API Consumers)                   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                              FASTAPI BACKEND ROUTER                               |
|              (app.py / CORS Middleware / Structured Logging / Health)              |
+-----------------------------------------------------------------------------------+
            |                                     |                                 |
            v                                     v                                 v
   [ GET /health ]                       [ POST /scan-text ]              [ POST /scan-file ]
            |                                     |                                 |
            v                                     v                                 v
+-----------------------+               +-------------------+             +-------------------+
| Service Health Status |               | Raw Text Input    |             | PDF / HTML / TXT  |
+-----------------------+               +-------------------+             +-------------------+
                                                  |                                 |
                                                  |                                 v
                                                  |                       +-------------------+
                                                  |                       | Layer Extractor   |
                                                  |                       |  - PDF metadata   |
                                                  |                       |  - White text     |
                                                  |                       |  - Microscopic    |
                                                  |                       |  - HTML comments  |
                                                  |                       |  - Hidden CSS     |
                                                  |                       +-------------------+
                                                  |                                 |
                                                  +----------------+----------------+
                                                                   |
                                                                   v
                                                  +-----------------------------------+
                                                  | Obfuscation Decoding Engine       |
                                                  |  - Zero-width character stripper  |
                                                  |  - Cyrillic/Greek homoglyphs      |
                                                  |  - Base64 / Hex / URL uncloaker   |
                                                  +-----------------------------------+
                                                                   |
                                                                   v
                                                  +-----------------------------------+
                                                  | Content Segmenter                 |
                                                  |  - Primary body text              |
                                                  |  - Hidden document layers         |
                                                  |  - Uncloaked decoded payloads     |
                                                  +-----------------------------------+
                                                                   |
                                                                   v
                                                  +-----------------------------------+
                                                  | Intelligence Layer                |
                                                  | Fine-Tuned DistilBERT Classifier  |
                                                  |  - Tokenizer Fast (max_len=256)   |
                                                  |  - Logit Softmax Probabilities    |
                                                  |  - Stealth Layer Heuristics       |
                                                  +-----------------------------------+
                                                                   |
                                                                   v
                                                  +-----------------------------------+
                                                  | Document Risk Aggregator         |
                                                  |  - Overall Label (Safe/Injection) |
                                                  |  - Max Confidence Score (%)       |
                                                  |  - Risk Hierarchy (High/Med/Low)  |
                                                  |  - Segment Breakdown & Warnings   |
                                                  +-----------------------------------+
                                                                   |
                                                                   v
                                                  +-----------------------------------+
                                                  | JSON Document Threat Report       |
                                                  +-----------------------------------+
```

---

## Pipeline Execution Flow

1. **Input Ingestion**: Supports raw strings via `/scan-text` and file bytes via `/scan-file` (`.pdf`, `.html`, `.txt`, `.md`).
2. **Layer Extraction**:
   - **PDF**: PyPDF metadata extraction + `pdfplumber` layout analysis separating visible text, white-on-white text ($RGB=(255,255,255)$), and microscopic font ($\le 1.5\text{pt}$).
   - **HTML**: BeautifulSoup parsing extracting `<!-- comments -->`, `<meta>` attributes, `alt` tags, hidden CSS elements (`display:none`, `visibility:hidden`, `opacity:0`, `color:transparent`), and rendered visible body text.
3. **Obfuscation Uncloaking**:
   - Strips zero-width unicode characters (`\u200B`, `\u200C`, `\uFEFF`).
   - Maps Cyrillic/Greek homoglyphs to Latin equivalents.
   - Uncloaks embedded Base64 strings (`[A-Za-z0-9+/]{12,}`), Hex sequences (`\x49\x67...`), and URL percent-encodings.
4. **DistilBERT Sequence Classification**:
   - Passes cleaned and uncloaked text segments through `DistilBertForSequenceClassification` (`distilbert-base-uncased` fine-tuned on 72,418 samples).
5. **Stealth Heuristic & Risk Aggregation**:
   - Flags stealth layers carrying prompt injection keywords with high-risk priority.
   - Aggregates overall document risk rating (`High`, `Medium`, `Low`) and returns a structured JSON payload to the client.
