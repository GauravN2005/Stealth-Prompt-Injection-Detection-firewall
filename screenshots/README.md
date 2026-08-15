# Demo Evidence & Screenshots Directory — Shield Firewall

This directory contains visual evidence, demo screenshots, and architectural flow diagrams for **Shield — AI-Driven Stealth Prompt Injection Detection Firewall**.

---

## Screenshot Inventory & Submission Evidence Guide

| Screenshot File | Description | Purpose / Milestone |
|---|---|---|
| `01_main_dashboard.png` | Overview of the Shield React UI dashboard | Demonstrates frontend user interface (Milestone 8) |
| `02_safe_text_scan.png` | Scan result for standard benign user prompt (Label: `Safe`, Risk: `Low`) | Demonstrates baseline classification capability (Milestone 5) |
| `03_injection_detection.png` | Scan result for direct prompt injection attempt (Label: `Injection`, Risk: `High`) | Demonstrates prompt injection detection (Milestone 5) |
| `04_obfuscated_payload_scan.png` | Uncloaking zero-width unicode anomalies & Base64 payloads | Demonstrates obfuscation decoding engine (Milestone 3 & 5) |
| `05_segment_inspector.png` | Segment inspector breaking down visible vs hidden document layers | Demonstrates document layer extraction (Milestone 3 & 8) |
| `06_api_swagger_docs.png` | FastAPI OpenAPI interactive documentation UI (`http://127.0.0.1:8000/docs`) | Demonstrates REST API engineering & OpenAPI spec (Milestone 8) |
| `07_test_suite_execution.png` | Execution output of pytest (`9 passed in 11.08s`) and `test_stealth.py` | Demonstrates engineering readiness & testing (Milestone 10) |
| `08_docker_build_run.png` | Terminal output of `docker build` and `docker run -p 8000:8000` | Demonstrates containerization & infrastructure readiness (Milestone 9) |

---

## Reproducing Demo Evidence Locally

To capture live screenshot evidence:

1. **Start Backend**:
   ```bash
   cd backend
   ..\.venv\Scripts\python.exe -m uvicorn app:app --port 8000
   ```
2. **Start Frontend Dashboard**:
   ```bash
   cd frontend
   npm run dev
   ```
3. **Run Automated Test Suite**:
   ```bash
   ..\.venv\Scripts\python.exe -m pytest tests/test_api.py
   ```
