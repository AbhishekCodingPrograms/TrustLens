# TrustLens Deployment & Security Audit Report

**Project:** TrustLens - Privacy-Gated AI with Verifiable Evidence  
**Datathon Theme:** AI Secured: Innovation Without Exposure  
**Target Platform:** IBM LinuxONE (`s390x`) Virtual Server / Enterprise Hybrid Cloud  
**Audit Date:** October 2026  
**Auditor:** DevOps, Application Security & LinuxONE Deployment Specialist  

---

## 1. Executive Audit Summary

A comprehensive code, security, and environment audit was performed on the **TrustLens** codebase. The application is an end-to-end, zero-trust document intelligence system that combines cryptographic integrity hashing, sensitive PII scanning and redaction, evidence-grounded BM25 vector retrieval (RAG), and immutable security auditing.

| Audit Category | Evaluation | Notes |
|---|---|---|
| **Core Functionality** | **Verified Complete** | Integrity verification, Privacy Gate, Grounded QA, and Audit Ledger operate cleanly. |
| **Test Suite** | **19/19 Passing** | All unit and security tests pass in under 6s using `.venv/Scripts/python.exe -m pytest tests -v`. |
| **LinuxONE (`s390x`) Compatibility** | **High Portability** | Zero reliance on compiled C++ vector databases (FAISS, ChromaDB). Uses pure-Python text extraction (`pypdf`), pure-Python PDF generation (`fpdf2`), and portable NumPy BM25. |
| **Secrets & Credential Hygiene** | **Clean** | No private keys, credentials, or `.env` files committed. `.gitignore` properly excludes `.env`, `*.pem`, `data/*.json`, and virtual environments. |
| **Network Safety** | **Hardened Needed** | Streamlit default should enforce `127.0.0.1` binding to avoid public IP exposure on `0.0.0.0`. SSH port-forwarding (`-L 8501:127.0.0.1:8501`) is the required access pattern. |
| **Access Control (RBAC)** | **Recommended Addition** | Add a lightweight, transparent 3-tier role switcher (`Security Officer`, `Auditor`, `Viewer`) to enforce operational boundaries. |
| **Prompt Injection Resilience** | **Recommended Hardening** | Wrap retrieved chunks inside explicit `<untrusted_document_context>` delimiters with system guardrails. |

---

## 2. Inventory of Implemented Components

```
IBM_IDEATHON/
├── app.py                     # Streamlit frontend & interactive orchestration (5 views)
├── config.py                  # Environment detection, regexes for 6 PII types, RAG config
├── integrity.py               # SHA-256 hashing, reference registration, tamper detection
├── privacy.py                 # Multi-pattern PII scanner, masking, selective redaction
├── document_qa.py             # Pure-Python BM25 vector retriever, chunker, & evidence Q&A
├── audit.py                   # Immutable security audit ledger & operational metrics engine
├── requirements.txt           # Portable dependencies (s390x-compatible)
├── Dockerfile                 # Multi-arch container definition (python:3.11-slim)
├── docker-compose.yml         # Container compose file
├── pytest.ini                 # Pytest discovery configuration
├── .env.example               # Zero-trust configuration template
├── .gitignore                 # Excludes caches, secrets, venvs, and local data
├── sample_docs/               # Synthetic test documents (Financial, Medical, Tampered)
├── docs/                      # Architectural docs, demo script, and pitch deck
└── tests/                     # 19 automated tests
```

---

## 3. Detailed Component Findings

### 3.1 Document Integrity Gate (`integrity.py`)
- **Byte-level Hashing:** SHA-256 digests are computed over raw bytes (`calculate_sha256`), completely decoupling hashing from text extraction or parsing.
- **Verification Logic:** Compares uploaded bytes against registered reference IDs or expected hashes, correctly returning `MATCH`, `MODIFIED`, or `NOT_REGISTERED`.
- **Honest Security Claims:** Explicit disclaimer included: hashes verify byte-level integrity relative to a trusted baseline; they do not attest to human authorship or legal creation time.
- **Ledger Storage:** Uses atomic write (`tmp` file replace) to `data/integrity_ledger.json`.

### 3.2 Privacy Gate & Redaction Engine (`privacy.py`)
- **Dual PDF Extraction:** Attempts `PyMuPDF` (`fitz`) first, with seamless fallback to pure-Python `pypdf`. Tested and verified working with pure `pypdf`.
- **Pattern Coverage:** Regular expressions for:
  - Email addresses (RFC-compliant patterns)
  - Phone numbers (US, international, Indian standard formats)
  - Credit card numbers (Visa, MasterCard, Amex, Discover)
  - SSN / National Tax IDs (`XXX-XX-XXXX`)
  - API Keys / Secret Tokens (`sk-...`, Bearer tokens, hex strings)
  - IPv4 Addresses
- **Preview Masking:** Safe preview masks (e.g. `j***@company.org`, `********4567`) displayed in UI tables without leaking sensitive text.
- **Selective Redaction:** Allows users to selectively check/uncheck finding IDs. Unselected items remain intact while approved items are tokenized (`[REDACTED_EMAIL_1]`).

### 3.3 Evidence-Grounded Document Q&A (`document_qa.py`)
- **Metadata-Preserving Chunking:** Chunks document pages strictly within page boundaries without cross-page blending, guaranteeing citation accuracy (`Page 1`, `Page 2`).
- **Portable BM25 Engine:** Pure-Python and NumPy implementation. Tokenizes text, eliminates English stopwords for substantive scoring, and applies BM25 weighting.
- **Anti-Hallucination Rejection:** Strictly rejects queries that lack substantive term matches or fail relevance thresholds, outputting:
  > *"The document does not contain sufficient verifiable evidence to answer this question."*
- **Model Isolation:** Confirmed via `test_privacy_gate_model_isolation` that raw confidential text is excluded from pipeline prompt payloads.

### 3.4 Security Auditor (`audit.py`)
- **Event Logging:** Records UTC timestamped events for `DOCUMENT_INGESTED`, `PRIVACY_SCAN`, `REDACTION_APPLIED`, `INTEGRITY_CHECK`, and `QA_QUERY`.
- **Zero Sensitive Data in Logs:** Logs store counts, hashes, categories, and latencies—never raw document content or detected secrets.
- **Metrics Calculation:** Metrics for the dashboard are calculated directly from logged event objects without hardcoding.

---

## 4. LinuxONE (`s390x`) Target Compatibility Analysis

- **Host Environment:** Tested and verified connectivity to IBM LinuxONE Community Cloud:
  - Architecture: `s390x` (IBM LinuxONE)
  - Operating System: Ubuntu 24.04.5 LTS
  - Python: `Python 3.12.3`
  - Available tools: `/usr/bin/python3`, `/usr/bin/pip3`, `/usr/bin/git`, `python3-venv`
- **Dependency Portability Matrix:**

| Package | LinuxONE Compatibility | Status / Fallback |
|---|---|---|
| `streamlit` | Compatible | Pure-Python + standard web assets. Runs inside standard venv. |
| `pypdf` | 100% Compatible | Pure-Python PDF parser. No C/C++ compilation required. |
| `fpdf2` | 100% Compatible | Pure-Python PDF synthesizer. Zero binary dependencies. |
| `numpy` | Compatible | Pre-built wheels available for s390x or via `python3-numpy` on Ubuntu 24.04. |
| `pandas` | Compatible | Pre-built wheels available for s390x or via `python3-pandas` on Ubuntu 24.04. |
| `python-dotenv` | 100% Compatible | Pure Python. |
| `pytest` | 100% Compatible | Pure Python. |
| `PyMuPDF` (`fitz`) | Optional / Conditional | Not required. Application gracefully falls back to `pypdf`. |

---

## 5. Required Actions for Datathon Readiness

1. **Phase 2 (Security Hardening):**
   - Add prompt injection defense: Wrap context inside `<untrusted_document_context>` tags with strict system guardrails.
   - Provide a pluggable/mockable LLM client interface in `document_qa.py` and a dedicated test inspecting the prompt received by the mock.
   - Implement lightweight 3-tier Role-Based Access Control (`Security Officer`, `Auditor`, `Viewer`) in `app.py`.
2. **Phase 3 & 4 (Packaging & Deployment):**
   - Write `scripts/package_for_linuxone.ps1` with strict exclusions (`.env`, `*.pem`, `.venv`, caches).
   - Write `scripts/deploy_linuxone.ps1` to upload and bootstrap the application on the LinuxONE VM.
   - Create `docs/linuxone_deployment.md` with complete, reproducible steps.
3. **Phase 5 & 6 (Testing & Verification):**
   - Verify localhost-only default (`127.0.0.1:8501`) and SSH tunneling.
   - Expand unit tests to verify prompt injection defense, RBAC permission checks, and archive hygiene.
   - Generate `docs/verification_report.md` capturing all local and remote test runs.
4. **Phase 7 (Submission Readiness):**
   - Finalize architecture, demo script, and submission checklist in `docs/`.
