# Engineering Decision Log — Shield Firewall

This document records key architectural, algorithmic, and infrastructure decisions made during the design and development of **Shield — AI-Driven Stealth Prompt Injection Detection Firewall**.

---

## 1. Model Selection: Fine-Tuned DistilBERT vs Generative LLM

### Decision
Selected **DistilBERT** (`distilbert-base-uncased`) fine-tuned on a 72,418 sample prompt injection dataset.

### Reason
- **Latency & Throughput**: DistilBERT evaluates text segments in under ~10-25ms on CPU, compared to 500ms–2000ms for local LLMs (Llama-3, Mistral) or cloud API calls.
- **Determinism**: Sequence classification outputs bounded logit probabilities (`Safe` vs `Injection`), preventing generative hallucinations or prompt injection attacks *against* the security model itself.
- **Edge Deployment**: Model weight footprint is ~267 MB, making it lightweight for containerized firewall sidecars.

### Alternative
Utilizing an LLM guardrail (e.g., Llama-Guard, GPT-4o mini, or Ollama local inference).

### Why Rejected
LLM-based guardrails suffer from high inference latency, high API costs, deployment complexity (requiring heavy GPU infrastructure), and susceptibility to indirect prompt injection payload recursion.

---

## 2. Architecture Strategy: Hybrid Preprocessing Engine + ML Classifier

### Decision
Implemented a **two-phase hybrid detection pipeline**: deterministic document extraction & obfuscation uncloaking followed by fine-tuned ML sequence classification.

### Reason
- **Stealth Payload Resilience**: Attackers routinely obfuscate prompt injections using white-on-white PDF text, zero-width unicode characters (`\u200B`), Base64/Hex encoding, or hidden HTML comments. Raw ML models fail on encoded/invisible text because tokenizers tokenize raw obfuscated strings into meaningless subwords.
- **Deterministic Uncloaking**: Decoding payloads *before* passing them to the classifier exposes hidden instructions to the ML model.

### Alternative
Passing raw, extracted file text directly to the ML model without layer extraction or obfuscation handling.

### Why Rejected
Raw text models miss hidden CSS elements (`display:none`), microscopic PDF text ($\le 1.5\text{pt}$), and Base64 encoded strings, leading to high false-negative rates on stealth payloads.

---

## 3. RAG Architecture Decision: Omission of RAG

### Decision
Explicitly decided **NOT to implement Retrieval-Augmented Generation (RAG)** for the Shield core firewall pipeline.

### Reason
- **Functional Scope**: Shield is a real-time inline security inspection firewall whose primary purpose is binary sequence classification (`Safe` vs `Injection`), document layer extraction, and risk assessment.
- **Complexity & Latency**: RAG requires vector database indexing (Chroma/FAISS), embedding models, and retrieval pipelines, which introduce unnecessary latency ($>200\text{ms}$) and infrastructure complexity without adding value to binary classification.

### Alternative
Building a vector database of past prompt injection signatures and retrieving top-$k$ context chunks prior to classification.

### Why Rejected
Vector similarity retrieval fails on novel prompt injection syntax and adds severe architectural bloat without improving single-segment ML sequence classification accuracy.

---

## 4. AI Agent Architecture Decision: Omission of Autonomous AI Agent

### Decision
Explicitly decided **NOT to implement an autonomous multi-step AI Agent** (e.g., LangChain/LangGraph agent loops).

### Reason
- **Deterministic Pipeline Security**: Security firewalls require deterministic, predictable execution flows ($A \rightarrow B \rightarrow C$). Autonomous agents introduced non-deterministic routing, tool selection loops, and execution delays.
- **Security Boundaries**: Allowing an AI agent to execute arbitrary tools to inspect security payloads exposes the agent to indirect prompt injection hijacking.

### Alternative
Using a ReAct agent framework to dynamically decide which document extractor tool to invoke.

### Why Rejected
Static MIME-type document routing (`.pdf` $\rightarrow$ `extract_pdf_layers`, `.html` $\rightarrow$ `extract_html_layers`) is faster ($O(1)$ lookup), 100% reliable, and completely immune to agent hijacking.

---

## 5. Model Distribution Strategy: Hugging Face Hub Download Script

### Decision
Stored model weights (`model.safetensors`, 267 MB) on Hugging Face Hub (`gaurav-nimbalkar/stealth-prompt-injection-detector`) and implemented `setup_model.py` for dynamic download.

### Reason
- **Git Repository Hygiene**: Keeps the git repository lightweight ($<5\text{MB}$), avoiding repository bloat and Git LFS bandwidth limits.
- **Automated Container Setup**: `Dockerfile` executes `python setup_model.py` during build, ensuring seamless container deployment.

### Alternative
Committing `model.safetensors` directly to the Git repository or Git LFS.

### Why Rejected
Directly committing 267 MB binary files causes slow git operations, clone bottlenecks, and deployment friction.

---

## 6. Backend Framework: FastAPI + Uvicorn

### Decision
Selected **FastAPI** with Uvicorn ASGI server.

### Reason
- High performance asynchronous I/O handling for non-blocking file uploads (`UploadFile`).
- Automatic OpenAPI/Swagger interactive documentation generation.
- Native Pydantic data validation for requests and responses.

### Alternative
Flask or Django REST Framework.

### Why Rejected
Flask lacks native async support for file streams and requires manual schema validation extensions. Django is heavyweight for a microservice firewall API.
