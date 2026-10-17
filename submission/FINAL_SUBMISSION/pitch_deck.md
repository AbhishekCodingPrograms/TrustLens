# TrustLens: Final Datathon Pitch Deck
**Competition:** IBM Z Datathon 2026  
**Challenge Theme:** AI Secured: Innovation Without Exposure  
**Target Platform:** IBM LinuxONE (`s390x`) Community Cloud & Enterprise Hybrid Clouds  

---

### Slide 1: Title & Value Proposition
- **Title:** TrustLens: Privacy-Gated AI with Verifiable Evidence
- **Tagline:** Innovation Without Exposure: Zero-Trust Document Intelligence for Enterprise Mainframes
- **Value Proposition:** An end-to-end document intelligence platform that cryptographically validates document integrity, intercepts and redacts confidential data before AI exposure, and grounds answers strictly in verifiable, page-cited evidence.
- **Presenter:** TrustLens Engineering Team

---

### Slide 2: Problem & User Impact
- **The Dilemma:** Highly regulated enterprises (banking, healthcare, legal, public sector) must analyze confidential documents (audits, contracts, patient trials) with AI without violating compliance.
- **The Three Core Vulnerabilities:**
  1. *Confidential Data Exposure:* Ingesting unredacted documents leaks PII, credit cards, tax IDs, and credentials to internal or external LLMs.
  2. *Ungrounded Hallucinations:* Conventional GenAI hallucinates plausible falsehoods with fabricated citations.
  3. *Silent Document Tampering:* Byte-level alterations to financial records go undetected prior to AI processing.
- **Impact:** Severe regulatory fines (GDPR, HIPAA, GLBA), compromised executive decisions, and loss of institutional trust.

---

### Slide 3: The TrustLens Solution
- **Zero-Trust Document Intelligence Architecture:**
  - **Cryptographic Document Integrity Gate:** Computes SHA-256 byte hashes, maintaining a reference ledger to detect alterations before ingestion.
  - **Pre-AI Privacy Gate:** Automatically detects sensitive entities across 6 classes and enforces selective, human-in-the-loop redaction.
  - **In-Memory AI Isolation:** The AI model is strictly quarantined, receiving ONLY sanitized text with prompt-injection defense tags.
  - **Evidence-Grounded RAG:** Pure-Python vector retrieval that pairs answers with exact page citations (`[Page 1]`) and rejects unsupported inquiries.
  - **Tamper-Evident Audit Trail:** Real operational metrics and immutable chronological logs recording every scan, redaction, and query.

---

### Slide 4: System Architecture & Data Flow
- **End-to-End Workflow:**
  1. *Upload:* PDF or TXT document uploaded via localhost-bound UI.
  2. *Parallel Integrity Gate:* SHA-256 digest calculated and compared against reference ledger (`MATCH` vs `MODIFIED`).
  3. *Text Extraction & Privacy Scan:* Multi-pattern regex scans text without external transmission.
  4. *Auditor Approval:* User reviews masked previews and approves redactions.
  5. *In-Memory Locking:* Document is sanitized; raw text is permanently isolated.
  6. *Evidence Retrieval:* Page-preserving chunking and BM25 relevance scoring.
  7. *Model Isolation Framing:* Context enclosed in `<untrusted_document_context>` with system anti-injection defense.
  8. *Grounded Synthesis:* Verbatim excerpts cited; non-evidenced questions rejected.
  9. *Audit Logging:* Event details appended to JSON audit ledger with actor roles.

---

### Slide 5: Privacy Gate & Sensitive-Data Protection
- **Multi-Class Entity Detection:**
  - Corporate & personal emails (`name@domain.com`)
  - Direct telephone & fax numbers (international and national formats)
  - Social Security Numbers & National Tax IDs (`XXX-XX-XXXX`)
  - Payment Cards (Visa, Mastercard, Amex, Discover Luhn-compliant formats)
  - API keys, JWT tokens, and private bearer credentials
  - IPv4 network addresses
- **Safe Auditor Preview:** Values are masked even in review tables (`j***@company.com`, `4***-****-****-1111`).
- **Selective Redaction:** Auditors select which entities to redact or preserve based on context.
- **Proven Quarantine:** Automated tests verify 100% of blocked sensitive tokens are absent from vector chunks and LLM prompts.

---

### Slide 6: Evidence-Grounded AI & Integrity Verification
- **Verifiable RAG Engine:**
  - Chunks text while strictly maintaining source page metadata (`page: 1`, `page: 2`). Never merges cross-page text.
  - Generates verifiable citations alongside answers: e.g., `Page 1 (CHUNK-001)`.
- **Anti-Hallucination & Prompt Injection Defense:**
  - Validates query relevance score >= threshold and substantive query token overlap.
  - Rejects unsupported questions with an explicit refusal: *"The document does not contain sufficient verifiable evidence to answer this question."*
  - Defends against indirect prompt injection via strict system instructions and XML containment tags.
- **Cryptographic Tamper Detection:**
  - Calculates standard SHA-256 digests over raw bytes.
  - Instantly flags single-byte modifications between baseline and incoming files.
  - *Honest Claim:* SHA-256 proves byte consistency with a baseline; it does not prove original human authorship.

---

### Slide 7: LinuxONE Deployment & Verified Test Evidence
- **Deployment Target:** IBM LinuxONE Community Cloud virtual server (`148.100.77.3`).
- **Hardware Architecture:** `s390x` (IBM z16 mainframe tuning `-mzarch -mtune=z16`, 3 vCPUs, 8 GB RAM, 50 GB disk).
- **Verified Native Performance:**
  - **Local Test Suite (Windows):** 32/32 automated unit/security tests passed in 1.75s.
  - **Remote Test Suite (LinuxONE `s390x`):** 32/32 automated unit/security tests passed natively in 0.27s.
  - **Complete 11-Step Journey:** 100% passed on LinuxONE (ingestion, redaction, payload isolation, citations, tamper detection, audit sanitization).
  - **Deep Pipeline Verification (`verify_linuxone.py`):** Verified SHA-256 match/tamper, 7/7 PII masking, grounded citations, and audit logging live on LinuxONE.
  - **Localhost Hardening:** Streamlit bound to `127.0.0.1:8501`, accessed exclusively through encrypted SSH port forwarding (`-L 8501:127.0.0.1:8501`). HTTP health check returned status code `200`.

---

### Slide 8: Limitations, Responsible AI & Future Work
- **Honest System Limitations:**
  - *Regex Boundaries:* Complex unstructured PII requires supplemental contextual NER in high-ambiguity edge cases.
  - *RBAC Scope:* Current implementation provides session-level role separation for demonstration; enterprise production requires directory federation.
  - *Hash Semantics:* Cryptographic digests attest to file integrity against reference records, not legal human authorship.
- **Future Enterprise Roadmap (Proposed):**
  - Federated enterprise identity integration (IBM RACF / LDAP / SAML SSO).
  - Hardware-assisted crypto acceleration using IBM Z CPACF (CP Assist for Cryptographic Function) on bare-metal deployments.
  - Immutable compliance storage integration with IBM WORM archive volumes.
  - Native IBM watsonx.ai on-premise governance connector.

---

### Slide 9: Conclusion & Value to Beneficiaries
- **Value to Financial & Banking Teams:** Verify audit integrity and summarize regulatory disclosures with zero PII exposure to third parties.
- **Value to Healthcare & Clinical Researchers:** Extract evidence from clinical trial reports while guaranteeing strict patient privacy.
- **Value to Legal & Compliance Officers:** Exportable, tamper-evident audit logs proving exact chain of custody and human redaction sign-off.
- **Datathon Commitment:**
  - 100% genuine code, zero fabricated benchmarks or false certifications.
  - Fully deployed, tested, and operational on IBM LinuxONE `s390x` today.
  - *Innovation without exposure is no longer a compromise.*
