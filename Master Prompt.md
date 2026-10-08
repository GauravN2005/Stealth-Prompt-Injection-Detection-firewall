# Master Prompt — Prepare Shield Repository for CODENIXIA AI/ML Internship Assessment 2026

You are working on my existing project:

**Shield — AI-Driven Stealth Prompt Injection Detection Firewall**

The project detects invisible and obfuscated prompt injection payloads hidden inside PDF, HTML, and plain-text content using document extraction, obfuscation detection/decoding, and a fine-tuned DistilBERT classifier. It has a FastAPI backend and React frontend.

This project is being submitted for the **CODENIXIA AI/ML Industry Internship Technical Selection Challenge – 2026**.

The official assessment requires ONE continuous project demonstrating:

1. Problem discovery and solution design
2. Data and knowledge strategy
3. Python data-processing pipeline
4. Data analysis and AI/ML fundamentals
5. ML/LLM intelligence layer
6. RAG where technically appropriate OR justification for not using RAG
7. AI Agent where technically appropriate OR justification for not using an Agent
8. Application/API
9. AI infrastructure/containerization
10. Testing, observability and engineering readiness

The assessment also requires:
- One GitHub repository
- README.md
- Architecture diagram
- Source code
- Dependencies
- Configuration instructions
- Data information
- AI/ML implementation
- Testing
- Docker/deployment files where applicable
- Screenshots/demo evidence
- AI_USAGE.md
- DECISION_LOG.md
- DEBUGGING_REPORT.md
- Reproducible setup
- Technical explanations
- At least two documented debugging problems

The final submission deadline is **16 August 2026 at 11:00 PM IST**.

## PRIMARY INSTRUCTION

DO NOT blindly rewrite or replace the existing project.

First inspect the ENTIRE repository and understand the existing implementation.

The repository has recently been updated and now includes:
- Model training notebook
- EDA notebook
- Existing backend
- Existing frontend
- Existing trained DistilBERT model setup
- Existing document extraction
- Existing obfuscation detection/decoding
- Existing tests
- Existing test documents

Preserve working functionality.

Do not introduce unnecessary technologies merely to make the project look more advanced.

The assessment explicitly values technically justified engineering decisions over technology count.

Therefore:

- DO NOT add RAG unless it genuinely improves Shield.
- DO NOT add an AI Agent unless it genuinely adds value.
- DO NOT add LangChain/LangGraph merely for appearance.
- DO NOT add Ollama/vLLM/Kubernetes unless genuinely required.
- DO NOT replace DistilBERT with an LLM unnecessarily.
- DO NOT rewrite the working architecture without a strong reason.

Instead, make the existing Shield project look and behave like a professional, assessment-ready AI/ML engineering project.

---

# PHASE 1 — FULL REPOSITORY AUDIT

Before modifying anything, inspect:

- Complete folder structure
- README.md
- Backend code
- Frontend code
- Model loading code
- Prediction code
- PDF extraction
- HTML extraction
- TXT processing
- Obfuscation decoder
- API endpoints
- Tests
- Test documents
- Model training notebook
- EDA notebook
- requirements files
- package.json
- configuration files
- model setup/download scripts
- Docker files if any
- gitignore
- environment files
- existing documentation

Understand how the entire system works.

Do not assume that something is missing just because it is not obvious from README.md.

---

# PHASE 2 — MAP THE EXISTING PROJECT TO CODENIXIA MILESTONES

Create an internal assessment matrix:

| Milestone | Requirement | Existing implementation | Missing | Action |
|---|---|---|---|---|
| 1 | Problem discovery | | | |
| 2 | Data strategy | | | |
| 3 | Python pipeline | | | |
| 4 | EDA + ML fundamentals | | | |
| 5 | Intelligence layer | | | |
| 6 | RAG | | | |
| 7 | Agent | | | |
| 8 | Application/API | | | |
| 9 | Docker/infrastructure | | | |
| 10 | Testing/observability | | | |

Use the actual repository implementation to fill this matrix.

Do not fabricate features.

---

# PHASE 3 — PROJECT ARCHITECTURE

Ensure the README clearly communicates this conceptual architecture:

User
↓
PDF / HTML / TXT Input
↓
Document Extraction
↓
Visible + Hidden Content Extraction
↓
Obfuscation Detection / Decoding
↓
Content Segmentation
↓
Fine-Tuned DistilBERT Classification
↓
Injection / Safe Classification
↓
Risk/Detection Result
↓
FastAPI
↓
React Dashboard

If the actual implementation differs, document the REAL architecture instead of inventing one.

Create/update an architecture diagram if necessary.

The architecture should clearly show:
- Input
- Extraction
- Obfuscation handling
- ML model
- Backend/API
- Frontend
- Output

---

# PHASE 4 — README.md

Rewrite/improve README.md so that it directly satisfies the CODENIXIA assessment.

Do not make it unnecessarily long or marketing-heavy.

Use a professional engineering-documentation style.

The README MUST contain the following sections:

## 1. Project Title

Shield — AI-Driven Stealth Prompt Injection Detection Firewall

## 2. Overview

Briefly explain what Shield does.

## 3. Problem Statement

Explain:
- What prompt injection is
- What stealth/obfuscated prompt injection means
- Why hidden payloads are dangerous
- Why normal text inspection can fail
- Why Shield is needed

Do not exaggerate claims.

## 4. Target Users

Identify realistic users such as:
- AI application developers
- AI security teams
- Security engineers
- Organizations processing untrusted documents
- LLM application developers

Only include users genuinely relevant to the project.

## 5. Why AI/ML is Required

Explain why a learned classifier is useful for semantic prompt-injection detection rather than relying only on handcrafted rules.

Also explain the role of deterministic preprocessing/obfuscation detection.

## 6. Proposed Solution

Explain the complete Shield workflow.

## 7. Key Features

Document the actual implemented features, including where applicable:
- PDF extraction
- HTML extraction
- TXT scanning
- Hidden-content detection
- Zero-width character handling
- Base64 decoding
- Hex decoding
- Homoglyph handling
- Per-segment classification
- FastAPI
- React dashboard
- Segment Inspector
- Test documents

Only mention features that actually exist in the code.

## 8. System Architecture

Include the architecture diagram.

## 9. End-to-End Workflow

Explain:

Input
→ Extraction
→ Obfuscation handling
→ Segmentation
→ Classification
→ Result
→ API
→ Dashboard

## 10. Technology Stack

Clearly categorize:

### ML
DistilBERT

### Backend
FastAPI / Uvicorn

### Document Processing
pdfplumber / pypdf / BeautifulSoup or actual libraries

### Frontend
React / Vite / Tailwind

### Testing
Actual testing framework/files used

### Deployment
Docker if implemented

Do not list unused technologies.

---

# PHASE 5 — DATA AND ML DOCUMENTATION

Because the Model Training Notebook and EDA Notebook have now been added, inspect them carefully.

Do NOT duplicate huge notebook outputs into README.

Instead summarize the important findings.

README should include:

## Dataset

Document:
- Dataset sources
- Dataset types
- Labels
- Number of samples
- Class distribution
- Data preprocessing
- Cleaning
- Deduplication if performed
- Train/validation/test split
- Tokenization
- Any balancing/imbalance handling actually performed

Do not invent values.

Use values from the actual notebook/code.

## EDA

Summarize:
- Dataset size
- Class distribution
- Important observations
- Data quality observations
- Any imbalance
- Relevant charts/visualizations

Mention the EDA notebook as supporting evidence.

## Model Training

Document:
- Base model
- Fine-tuning approach
- Input format
- Classification labels
- Training configuration
- Evaluation method
- Important hyperparameters where useful

## Evaluation

Include actual results from the training/evaluation notebook.

If available, document:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

DO NOT claim perfect performance unless it is actually supported by the final evaluation methodology.

Also explain potential limitations such as:
- Dataset bias
- Distribution shift
- False positives
- False negatives
- Unseen obfuscation techniques
- Adversarial evolution

---

# PHASE 6 — RAG DECISION

Do NOT add RAG automatically.

Assess the actual Shield use case.

If RAG does not provide meaningful value, add a section:

## Why RAG is Not Used

Explain that Shield's primary task is security classification and stealth-content extraction rather than knowledge-grounded question answering.

Explain why vector retrieval would introduce unnecessary complexity for the current objective.

If you determine that RAG genuinely improves a clearly defined feature, explain the reason before implementing it.

Do not implement RAG just because CODENIXIA mentions it.

---

# PHASE 7 — AI AGENT DECISION

Do NOT add an AI Agent just to satisfy terminology.

If an Agent does not meaningfully improve Shield, add:

## Why an AI Agent is Not Used

Explain that the current workflow is a deterministic security-analysis pipeline and does not require autonomous multi-step decision-making or tool orchestration.

If you determine an Agent is genuinely useful, first document the use case and architecture before implementing it.

---

# PHASE 8 — API DOCUMENTATION

Inspect the actual FastAPI implementation.

Document every implemented endpoint.

For each endpoint provide:

- Method
- Endpoint
- Purpose
- Input
- Output
- Error behavior
- Example request if useful

Ensure the documented API exactly matches the actual implementation.

At minimum inspect whether these exist:

GET /
POST /predict
POST /scan-text
POST /scan-file

If `/health` does not exist and adding it is safe and useful, add a proper:

GET /health

It should return meaningful service/model status.

Do not break existing endpoints.

---

# PHASE 9 — ERROR HANDLING

Audit the backend for:

- Invalid file types
- Empty files
- Malformed PDF
- Malformed HTML
- Invalid request body
- Missing file
- Model loading failure
- Prediction failure
- Decoding errors
- Oversized inputs where applicable

Ensure the API returns clear, controlled errors instead of crashing.

Do not expose internal stack traces to normal API users.

---

# PHASE 10 — LOGGING / OBSERVABILITY

Add meaningful logging if not already present.

Log useful events such as:

- Request received
- File type
- Processing stage
- Number of segments
- Obfuscation detection
- Prediction completion
- Processing errors
- Important timing information where appropriate

Do not log secrets or sensitive user content unnecessarily.

---

# PHASE 11 — TESTING

Inspect existing tests first.

Do not delete existing tests.

Expand tests where appropriate.

At minimum test the core functionality:

1. Safe plain text
2. Direct prompt injection
3. Zero-width obfuscation
4. Base64 obfuscation
5. Hex obfuscation
6. Hidden HTML
7. HTML comments
8. PDF metadata
9. Invalid file
10. Unsupported file type
11. API error handling
12. Model loading behavior

Use actual project behavior.

Tests must be reproducible.

Make sure tests can be run from documented commands.

---

# PHASE 12 — DOCKER / REPRODUCIBILITY

Inspect whether Docker already exists.

If not, create an appropriate Docker setup.

At minimum consider:

- Dockerfile
- `.dockerignore`
- dependency installation
- environment configuration
- model setup/download
- backend execution

If the frontend should also be containerized, decide whether this adds useful value.

Prefer a simple architecture that can actually be explained during technical defense.

The final README must explain:

1. Local setup
2. Model setup
3. Backend setup
4. Frontend setup
5. Docker setup
6. Running the application
7. Running tests

Do not commit large model binaries if the current architecture already uses Hugging Face/model download setup.

Use the existing model download approach if it works.

---

# PHASE 13 — SECURITY / SECRET AUDIT

Before finalizing:

Search the repository for:

- API keys
- passwords
- tokens
- private credentials
- `.env`
- secrets
- personal access tokens
- hardcoded production credentials

Never commit secrets.

Create/update:

`.gitignore`

and, if necessary:

`.env.example`

Use placeholders.

---

# PHASE 14 — AI_USAGE.md

Create:

`AI_USAGE.md`

Document honestly:

## AI Tools Used

Examples only if actually used:
- ChatGPT
- Gemini
- Claude
- GitHub Copilot
- Antigravity

For each tool document:
- Tool
- Purpose
- Type of assistance
- Important changes made by the student

Clearly state that the final implementation was reviewed, modified and tested by the student.

Do not fabricate AI usage.

---

# PHASE 15 — DECISION_LOG.md

Create:

`DECISION_LOG.md`

Document major engineering decisions.

Use this format:

### Decision
What was selected?

### Reason
Why?

### Alternative
What alternatives were considered?

### Why Rejected
Why wasn't the alternative selected?

Include decisions such as applicable:
- DistilBERT selection
- FastAPI
- React
- Local/cloud model strategy
- Document extraction libraries
- Obfuscation handling strategy
- RAG decision
- Agent decision
- Docker decision
- Model hosting/download strategy

Only document decisions that actually occurred or are genuinely made during this cleanup.

---

# PHASE 16 — DEBUGGING_REPORT.md

Create:

`DEBUGGING_REPORT.md`

Document at least TWO REAL technical problems encountered during development.

For each:

### Problem
What failed?

### Error / Symptom
What happened?

### Investigation
How was it investigated?

### Root Cause
What caused it?

### Solution
What was changed?

### Verification
How was the fix verified?

Use actual project development history wherever available.

DO NOT fabricate debugging incidents.

---

# PHASE 17 — SCREENSHOTS / DEMO EVIDENCE

Inspect whether useful screenshots already exist.

If not, identify what screenshots should be captured.

Recommended evidence:

1. Main Shield dashboard
2. Safe input result
3. Injection detection result
4. Hidden/obfuscated payload detection
5. Segment Inspector
6. API response
7. Test execution
8. Architecture diagram

Do not create fake screenshots.

If screenshots cannot be automatically generated, add a clear `screenshots/` structure and document what should be captured.

---

# PHASE 18 — PROJECT STRUCTURE CLEANUP

Make the repository professional.

A structure similar to this is preferred, but adapt it to the actual project:

shield/
│
├── README.md
├── AI_USAGE.md
├── DECISION_LOG.md
├── DEBUGGING_REPORT.md
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
│
├── backend/
│   ├── app.py
│   ├── model.py
│   ├── predict.py
│   ├── extractors.py
│   ├── obfuscation.py
│   ├── ...
│
├── frontend/
│   ├── ...
│
├── notebooks/
│   ├── model_training.ipynb
│   └── EDA.ipynb
│
├── tests/
│   └── ...
│
├── test_documents/
│   └── ...
│
├── architecture/
│   └── architecture.png
│
└── screenshots/
    └── ...

DO NOT blindly move files if doing so would break imports or execution.

Preserve the working project structure where possible.

---

# PHASE 19 — NOTEBOOKS

Inspect the Model Training Notebook and EDA Notebook.

Make sure they are:

- Clearly named
- Understandable
- Reproducible where possible
- Free of irrelevant cells
- Free of unnecessary debugging output
- Properly titled
- Have clear sections
- Explain important steps
- Include meaningful results

Do not modify experimental results merely to make them look better.

Do not remove important evidence.

---

# PHASE 20 — FINAL README ASSESSMENT SECTION

Add a section:

## CODENIXIA Assessment Alignment

Create a concise table:

| Milestone | Shield Implementation |
|---|---|
| 1. Problem Discovery | ... |
| 2. Data & Knowledge Strategy | ... |
| 3. Python Processing | ... |
| 4. Data Analysis & ML | ... |
| 5. Intelligence Layer | ... |
| 6. RAG | Used / Not Used + reason |
| 7. Agent | Used / Not Used + reason |
| 8. Application/API | ... |
| 9. Infrastructure | ... |
| 10. Testing & Engineering | ... |

This section should reference actual project components.

Do not claim a milestone is complete if it is not.

---

# PHASE 21 — FINAL SUBMISSION CHECK

Before considering the project complete, verify:

### Code
- No obvious bugs
- Backend starts
- Frontend starts
- APIs work
- Model loads
- PDF scanning works
- HTML scanning works
- TXT scanning works
- Obfuscation handling works

### ML
- Model exists/is downloadable
- Model loading works
- Prediction works
- Evaluation results documented
- Limitations documented

### Testing
- Tests execute successfully
- Invalid inputs handled
- API errors handled
- Health endpoint works if implemented

### Docker
- Docker build succeeds
- Application can run using documented instructions
- Model setup is documented

### Documentation
- README complete
- AI_USAGE.md complete
- DECISION_LOG.md complete
- DEBUGGING_REPORT.md complete
- Architecture diagram present
- Screenshots/demo evidence present or clearly structured

### Security
- No secrets
- `.gitignore` correct
- `.env.example` if needed

### GitHub
- Repository structure clean
- No unnecessary generated files
- No huge accidental files
- Model binary is handled appropriately
- README links work
- Setup instructions are accurate

---

# IMPORTANT CONSTRAINTS

1. Do not fabricate results.
2. Do not fabricate datasets.
3. Do not fabricate debugging problems.
4. Do not fabricate AI usage.
5. Do not claim a feature exists unless it actually exists.
6. Do not add RAG unnecessarily.
7. Do not add an Agent unnecessarily.
8. Do not replace the existing model without a strong reason.
9. Do not break existing working functionality.
10. Do not remove useful existing functionality.
11. Do not expose secrets.
12. Do not commit the 267 MB model file if the existing Hugging Face download approach is working.
13. Do not make unsupported claims such as "100% secure" or "detects all prompt injections."
14. Prefer simple, explainable engineering decisions.
15. Every change must be testable.
16. The final project must be something the student can explain and modify during a technical defense.

---

# FINAL OUTPUT REQUIRED FROM YOU

After making the changes, provide a concise final report containing:

## 1. Changes Made
List every important change.

## 2. Files Created
List all new files.

## 3. Files Modified
List important modified files.

## 4. CODENIXIA Milestone Status

Use:

- ✅ Complete
- ⚠️ Partial
- ❌ Not Complete

for Milestones 1–10.

## 5. Remaining Issues

Clearly list anything that still needs manual action.

## 6. Testing Results

Report the actual tests executed and their results.

## 7. Docker Result

State whether Docker build/run was actually tested.

## 8. Final Submission Checklist

Provide:

- README
- AI_USAGE.md
- DECISION_LOG.md
- DEBUGGING_REPORT.md
- Architecture
- EDA
- Model training
- Testing
- Docker
- Screenshots
- GitHub readiness

Do not say "submission ready" unless the repository has actually been checked against all requirements.

The goal is to make the EXISTING Shield project a professional, technically defensible and CODENIXIA-assessment-ready submission without unnecessary feature creep.