# TrustLens: Datathon Submission Checklist & Form Answers

**Competition:** IBM Z Datathon 2026  
**Theme:** AI Secured: Innovation Without Exposure  
**Track:** Document Intelligence & Enterprise Mainframe Security  
**Target Platform:** IBM LinuxONE (`s390x`) & Hybrid Multi-Cloud  

---

## 1. Submission Deliverables Checklist

| Deliverable | Item / Location | Status | Action Required by Submitter |
|---|---|---|---|
| **Clean Source Archive** | `dist/trustlens_s390x_deploy.tar.gz` (58.53 KB, SHA-256 verified) | ✅ Ready | Upload `dist/trustlens_s390x_deploy.tar.gz` or push to your personal GitHub repository. |
| **GitHub Repository** | User repository (to be published by submitter) | ⏳ Ready for push | Run `git init`, add remote, and push project root. *(Remember: `.env` and `.pem` are excluded by `.gitignore`)*. |
| **Architecture Documentation** | `docs/architecture.md` | ✅ Complete | Review technical design, Mermaid diagrams, and threat model. |
| **Pitch Deck Slides** | `docs/pitch_deck.md` | ✅ Complete | Export markdown to PDF or import into PowerPoint/Keynote for slide presentation. |
| **3-Minute Video Script** | `docs/demo_script.md` | ✅ Complete | Record 3-minute video following the step-by-step walkthrough script and upload to YouTube/Vimeo. |
| **LinuxONE Deployment Guide** | `docs/linuxone_deployment.md` | ✅ Complete | Documented setup, transfer, and verification steps on Ubuntu 24.04 `s390x`. |
| **Verification & Audit Reports** | `docs/deployment_audit.md` & `docs/verification_report.md` | ✅ Complete | Detailed logs of local test passes, secret scans, and remote LinuxONE inspection. |
| **Automated Deployment Scripts** | `scripts/package_for_linuxone.ps1` & `scripts/deploy_linuxone.ps1` | ✅ Complete | Automated packaging and SCP/SSH deployment scripts for Windows PowerShell. |

---

## 2. Standard Hackathon Submission Form Answers

Below are clear, concise, and technically grounded answers tailored for the IBM Z Datathon 2026 submission form:

### Q1: Project Title & Tagline
- **Project Title:** TrustLens: Privacy-Gated AI with Verifiable Evidence
- **Tagline:** Innovation Without Exposure: Zero-Trust Document Intelligence for Enterprise Mainframes

### Q2: Problem Statement
Organizations operating in highly regulated domains—such as banking, healthcare, legal, and public sector—face an urgent dilemma: **How can enterprise teams leverage Generative AI for document intelligence without exposing sensitive personal identifiable information (PII), leaking credentials, or accepting hallucinated citations?** Sending raw confidential audits or medical records to external or internal LLMs risks severe compliance violations (GDPR, HIPAA, GLBA), while ungrounded generative models frequently fabricate plausible-sounding falsehoods. Furthermore, without cryptographic baselining, unauthorized byte-level alterations to financial records go completely undetected before AI processing.

### Q3: Technical Solution & Architecture
TrustLens implements an end-to-end, zero-trust document intelligence architecture:
1. **Cryptographic Document Integrity Gate (`integrity.py`):** Computes SHA-256 digests over raw bytes prior to parsing, maintaining an immutable baseline ledger to flag unauthorized modifications (`MATCH` vs `MODIFIED`).
2. **Privacy Gate & Selective Redaction (`privacy.py`):** Scans extracted text across 6 entity classes (Emails, Phones, SSNs/Tax IDs, Credit Cards, API Keys, IPv4 addresses) with safe preview masking. Users approve selective redactions, generating a sanitized in-memory representation.
3. **Evidence-Grounded RAG Engine (`document_qa.py`):** Chunks text while strictly preserving page boundaries, indexes passages using a pure-Python + NumPy BM25 retriever, and frames evidence within `<untrusted_document_context>` delimiters with strict system prompt injection defenses. It answers questions using verbatim excerpts with exact page citations (`[Page 1]`, `[Page 2]`) and **strictly refuses to answer** when verifiable evidence is absent.
4. **Security Auditor (`audit.py`):** Records immutable, chronological JSON audit trails of every ingestion, scan, redaction, and query, calculating real operational metrics and measured retrieval latencies without hardcoding.
5. **Role-Based Access Control (`config.py` & `app.py`):** Enforces separation of duties across Security Officers, Compliance Auditors, and Restricted Viewers.

### Q4: How does this utilize IBM LinuxONE / zSystems capabilities?
- **Guaranteed `s390x` Portability:** Rather than relying on fragile, uncompiled C++ vector databases (FAISS, ChromaDB, hnswlib) that fail to compile or suffer byte-ordering issues on Big-Endian `s390x`, TrustLens uses pure-Python text extraction (`pypdf`), pure-Python PDF synthesis (`fpdf2`), and NumPy-powered BM25 retrieval.
- **Enclave Execution & Localhost Hardening:** Built to run entirely on-premise within an IBM LinuxONE virtual server. Streamlit binds strictly to `127.0.0.1:8501`, preventing public internet exposure and allowing enterprise access exclusively via encrypted SSH port-forwarding tunnels (`-L 8501:127.0.0.1:8501`).
- **Cryptographic Readiness:** Baseline digests utilize standard SHA-256 primitives, directly compatible with IBM Z CPACF (CP Assist for Cryptographic Function) hardware acceleration.

### Q5: What open-source tools and frameworks were used?
- **Python Standard Library:** `hashlib` (SHA-256 cryptographic digests), `re` (regex pattern scanning), `json` (atomic ledger persistence), `platform` (architecture detection).
- **Streamlit:** Interactive web application framework and operational dashboard.
- **pypdf & fpdf2:** Pure-Python PDF parsing and document synthesis.
- **NumPy & Pandas:** High-performance term scoring, array operations, and tabular audit rendering.
- **pytest:** Automated test execution framework (27/27 tests passed).

### Q6: Security & Privacy Guarantees (Honest Claims)
- **Model Isolation Proof:** Confirmed via automated test `test_privacy_gate_model_isolation` and `test_mocked_model_prompt_payload_inspection`: blocked sensitive PII strings never appear in vector chunks or model prompt payloads.
- **Integrity Disclaimers:** Hashes verify byte-level consistency relative to a trusted reference; they do not attest to original human authorship.
- **Sanitized Audit Trails:** Audit events log counts, hashes, categories, and latencies—never raw document content or detected secrets.
