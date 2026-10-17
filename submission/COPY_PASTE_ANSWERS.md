# IBM Z Datathon 2026: Official Portal Submission Copy-Paste Guide

**Platform Portal:** [hack2skill.com/event/datathon-2026](https://hack2skill.com/event/datathon-2026)  
**Project Name:** TrustLens: Privacy-Gated AI with Verifiable Evidence  
**Mandatory Event Code:** `SSF2026` (included in Project Description)  
**Status:** 100% Verified, Tested & Deployment-Ready  

---

### Field 1: Challenges *
**Select from dropdown:**
```text
AI Secured: Innovation Without Exposure
```

---

### Field 2: What is the Problem you are trying to solve? *
*(Character count: 659 / 1024 max — strictly compliant)*

```text
Enterprises in banking, healthcare, and government handle sensitive documents containing customer PII, clinical data, and confidential financials. Today, using LLMs on these documents creates two major hazards: accidental data leakage when raw sensitive text enters model prompts, and hallucinations where AI invents false facts with fabricated citations.

Additionally, most document pipelines lack pre-ingestion cryptographic checks, leaving organizations unable to detect whether a file was modified or corrupted before analysis. This forces compliance teams to either block AI adoption entirely or risk severe regulatory fines under GDPR, HIPAA, and GLBA.
```

---

### Field 3: How are you planning to solve the problem? (Brief Overview) *
*(Character count: 981 / 1024 max — strictly compliant, includes mandatory event code `SSF2026`)*

```text
Event code: SSF2026. TrustLens is a zero-trust document intelligence system built for high-security environments.

Architecture & Implementation:
1. Integrity Gate: Before parsing, TrustLens calculates a SHA-256 digest over raw bytes and compares it against a registered baseline, catching file tampering immediately (MATCH vs MODIFIED).
2. Privacy Gate: Scans text for emails, phone numbers, credit cards, SSNs, IPs, and API keys. Compliance officers review matches and approve redactions, producing a sanitized in-memory representation.
3. Grounded Retrieval & Model Isolation: Text is chunked with strict page-boundary preservation. An in-memory BM25 engine retrieves relevant passages into an untrusted prompt enclosure (<untrusted_document_context>). The model answers strictly from cited text with exact page numbers ([Page 1]) and refuses questions when evidence is lacking.
4. Audit Trail: All scans, hash checks, and queries are recorded in an immutable JSON audit ledger.
```

---

### Field 4: How does your solution leverage IBM Z / LinuxONE technologies? *
*(Character count: 996 / 1024 max — strictly compliant)*

```text
TrustLens is deployed and tested natively on an IBM LinuxONE Community Cloud virtual server (148.100.77.3, s390x, Ubuntu 24.04 LTS):
- Architecture Portability: We deliberately engineered TrustLens using pure-Python and precompiled Ubuntu Noble libraries (pypdf, fpdf2, NumPy, Pandas, Streamlit) to avoid C++ Big-Endian byte-order and wheel compilation failures common to standard vector databases on s390x.
- Enterprise Security Posture: The service binds strictly to 127.0.0.1:8501 with zero public ports exposed. Mainframe operators access the interface through authenticated SSH port forwarding (-L 8501:127.0.0.1:8501), ensuring a private attack surface.
- High-Throughput Cryptography: Our SHA-256 hashing architecture is designed to map directly to IBM Z CPACF (CP Assist for Cryptographic Function) hardware acceleration for wire-speed document validation.
- Validated Performance: All 32 automated unit, security, and boundary tests execute natively on the mainframe CPU in 0.28 seconds.
```

---

### Field 5: What value does your solution deliver, and who will benefit from it? *
*(Character count: 897 / 1024 max — strictly compliant)*

```text
TrustLens enables risk-averse enterprises to adopt document AI without compromising privacy:
- Financial Institutions: Auditors review loan portfolios, audit reports, and balance sheets knowing customer account numbers, card details, and tax IDs are masked before reaching the model.
- Healthcare Providers: Clinical research teams can summarize patient case studies and trial documents with verifiable citations while maintaining strict HIPAA compliance.
- Legal & Compliance Teams: Contract analysts get verifiable page-level evidence for every claim and a cryptographic guarantee that analyzed contracts were not tampered with. If an answer cannot be proven from the text, the system refuses to answer rather than hallucinating.
- Concrete ROI: Eliminates manual redaction overhead, prevents regulatory penalties, and gives compliance officers a tamper-evident audit ledger for non-repudiation.
```

---

### Field 6: Upload your pitch deck in PDF Format
**File to drag and drop:**
- `submission/FINAL_SUBMISSION/trustlens_pitch_deck.pdf`
- *Details:* Exactly **15.25 KB** (15,611 bytes), 9 slides, landscape orientation, well below the 5 MB ceiling.

---

### Field 7: Github Link of your Project / Link of your Zip File (make sure its publicly accessible!) *
```text
https://github.com/AbhishekCodingPrograms/TrustLens

Live Interactive Demo:
https://trustlens-abhishek.streamlit.app/
```

---

### Field 8: Video Submission Link *
```text
https://youtu.be/<your-video-id>
```
*(Or Vimeo / unlisted YouTube link. Recommended format: 720p or 1080p, maximum 3 minutes).*

---

### Field 9: Share the link to your pitch deck in PDF Format (if not able to upload the file)
```text
https://raw.githubusercontent.com/AbhishekCodingPrograms/TrustLens/main/submission/FINAL_SUBMISSION/trustlens_pitch_deck.pdf
```

---

### Field 10: Link to all open-source resources used *
*(Character count: 561 / 1024 max — strictly compliant with direct URLs)*

```text
Direct URLs to open-source libraries used in TrustLens:
- Streamlit (Web Dashboard): https://github.com/streamlit/streamlit
- PyPDF (Pure-Python PDF parser): https://github.com/py-pdf/pypdf
- fpdf2 (Pure-Python PDF generation): https://github.com/py-pdf/fpdf2
- NumPy (BM25 matrix indexing): https://github.com/numpy/numpy
- Pandas (Tabular audit log views): https://github.com/pandas-dev/pandas
- Pytest (Automated test framework): https://github.com/pytest-dev/pytest
- Python Standard Library (hashlib, re, json, platform): https://docs.python.org/3/library/
```

---

### Field 11: Any other document that you would like to share like the solution flowchart or architecture diagram
```text
Live Interactive Web Application:
https://trustlens-abhishek.streamlit.app/

Interactive System Architecture & Data Flow Diagram:
https://github.com/AbhishekCodingPrograms/TrustLens/blob/main/submission/FINAL_SUBMISSION/architecture_diagram.html

Detailed LinuxONE Verification & Benchmark Report:
https://github.com/AbhishekCodingPrograms/TrustLens/blob/main/submission/FINAL_SUBMISSION/FINAL_STATUS.md
```

