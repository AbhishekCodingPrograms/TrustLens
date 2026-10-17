# TrustLens: Final Hackathon Form Submission Answers
**Competition:** IBM Z Datathon 2026  
**Theme:** AI Secured: Innovation Without Exposure  

---

> [!IMPORTANT]
> **Action Required by Submitter Before Submission**:
> 1. Push your local project to your public GitHub repository and insert the URL in **Field 6**.
> 2. Record your 3-minute video using `demo_script.md`, upload it to YouTube/Vimeo/Drive, and insert the URL in **Field 7**.

---

### Field 1: Selected Challenge & Track
```text
Challenge Track: AI Secured: Innovation Without Exposure
Project Title: TrustLens: Privacy-Gated AI with Verifiable Evidence
Tagline: Zero-Trust Document Intelligence for Enterprise Mainframes
Event Code: SSF2026
```

---

### Field 2: Problem Statement
```text
Enterprises in highly regulated domains—banking, healthcare, legal, and public sector—face an urgent compliance crisis when adopting Generative AI for document analysis. Ingesting raw financial audits, clinical trials, or contracts into AI models exposes sensitive personal identifiable information (PII), credit cards, and trade secrets to model context windows. Furthermore, conventional generative AI regularly hallucinates plausible falsehoods with fabricated citations. Lastly, without pre-ingestion cryptographic integrity verification, unauthorized byte-level file tampering or corruption goes completely undetected. Organizations are currently forced to either ban AI or risk severe compliance violations.
```

---

### Field 3: Project Overview, Architecture & Tools
```text
[Event Code: SSF2026] TrustLens implements an end-to-end, zero-trust document intelligence architecture:
1. Cryptographic Document Integrity Gate (integrity.py): Computes SHA-256 digests over raw bytes before parsing, maintaining an atomic reference ledger to detect tampering (MATCH vs MODIFIED).
2. Privacy Gate & Selective Masking (privacy.py): Scans extracted text across 6 entity classes (Emails, Phones, SSNs, Credit Cards, API Keys, IPs) with safe preview masking. Auditors approve redactions, generating a sanitized in-memory representation.
3. Grounded RAG & Model Isolation (document_qa.py): Chunks text preserving page boundaries, indexes passages via portable NumPy BM25 retrieval, and frames evidence inside <untrusted_document_context> tags with strict prompt-injection defenses. Answers questions with exact page citations ([Page 1]) and strictly rejects unsupported questions.
4. Tamper-Evident Audit Trail (audit.py): Logs all lifecycle events with actor roles.
```


---

### Field 4: How IBM Z / LinuxONE is Used
```text
TrustLens is deployed and verified natively on an IBM LinuxONE Community Cloud virtual server (148.100.77.3) running Ubuntu 24.04.5 LTS on the s390x IBM zArchitecture:
- Guaranteed s390x Portability: TrustLens eliminates reliance on fragile, uncompiled C++ vector databases that fail or suffer byte-ordering issues on Big-Endian mainframes. Text extraction (pypdf), synthesis (fpdf2), and BM25 indexing execute with zero external binary compilation overhead.
- Localhost Hardening: The application binds strictly to 127.0.0.1:8501 and is accessed exclusively via authenticated SSH port forwarding (-L 8501:127.0.0.1:8501), ensuring zero public internet attack surface.
- Native Mainframe Speed: All 32 automated unit, security, and RBAC tests execute directly on the mainframe CPU in 0.26 seconds.
- Cryptographic Alignment: SHA-256 hashing directly aligns with IBM Z CPACF (CP Assist for Cryptographic Function) hardware instructions for production scaling.
```

---

### Field 5: Value & Intended Beneficiaries
```text
TrustLens delivers measurable, verifiable value across three core beneficiary groups:
1. Banking & Financial Institutions: Compliance officers verify balance sheet and audit report integrity before AI processing, ensuring zero customer account numbers or PII leak into model context windows under GDPR and GLBA.
2. Healthcare & Clinical Research: Medical research teams query complex multi-page clinical trial reports with guaranteed patient privacy and verifiable source citations under HIPAA guidelines.
3. Legal & Enterprise Audit Teams: Eliminates hallucination risk in contract review. Every answer is tied to an explicit page citation (Page 1, Chunk 1), while unauthorized contract tampering triggers immediate security alerts. Complete JSON audit logs provide non-repudiation for regulatory investigations.
```

---

### Field 6: Public Source Code Repository URL
```text
[ACTION REQUIRED: Insert your public GitHub repository URL here]
Example: https://github.com/<your-username>/TrustLens
```
*(Note: Excludes all credentials and keys via .gitignore; verified clean release).*

---

### Field 7: Video Demonstration URL
```text
[ACTION REQUIRED: Insert your 3-minute video URL here]
Example: https://youtu.be/<your-video-id> (or Vimeo / unlisted Google Drive link)
```
*(Recorded using the step-by-step walkthrough script in demo_script.md).*

---

### Field 8: Pitch Deck Location
```text
File: trustlens_pitch_deck.pdf (15.25 KB, 9 landscape slides, fully compliant with <5MB limit)
Markdown Source: pitch_deck.md
```

---

### Field 9: Open-Source Resources Used
```text
- Python Standard Library: hashlib (SHA-256 hashing), re (regex privacy pattern scanning), json (atomic persistence), platform (s390x architecture detection).
- Streamlit: Operational dashboard and user review interface.
- pypdf: Pure-Python PDF parsing with page tracking.
- fpdf2: Pure-Python PDF generation for pitch deck and sanitized document exports.
- NumPy & Pandas: BM25 term frequency matrix operations and tabular audit trail views.
- pytest: Automated test suite verification framework.
```

---

### Field 10: Supporting Documentation
```text
- System Architecture Diagram: architecture_diagram.mmd & architecture_diagram.html
- LinuxONE Verification Log: docs/verification_report.md
- Final Security & Deployment Audit: final_test_report.md
- Video Demo Script: demo_script.md
- LinuxONE Deployment Guide: docs/linuxone_deployment.md
- Release Verification Report: release_report.md
```
