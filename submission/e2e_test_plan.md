# TrustLens: End-to-End Test Plan & Verification Matrix
**Competition:** IBM Z Datathon 2026  
**Theme:** AI Secured: Innovation Without Exposure  
**Platform Target:** IBM LinuxONE Community Cloud (`s390x`) & Local Workstations  

---

## 1. Overview & Testing Philosophy

This End-to-End (E2E) Test Plan defines the formal validation procedures for **TrustLens: Privacy-Gated AI with Verifiable Evidence**. Testing enforces zero-trust boundaries:
1. **Cryptographic Proofs**: Byte-level SHA-256 consistency verification.
2. **Deterministic Privacy Quarantines**: 100% masking of sensitive values before model transmission.
3. **Evidence Grounding**: Strict requirement that every AI-generated claim cite a physical source page.
4. **Sanitized Telemetry**: Zero leakage of raw documents or secrets in persistent logs.

All test procedures below have been executed and verified across both Windows local and native IBM LinuxONE (`s390x`) environments.

---

## 2. Comprehensive 13-Workflow Test Matrix

| ID | Workflow Description | Target Component | Automated Test Reference | Status |
|---|---|---|---|---|
| **E2E-01** | Application Startup & Configuration Validation | `config.py`, `app.py` | `test_role_definitions_exist` | ✅ PASS |
| **E2E-02** | Uploading a Valid Synthetic PDF/TXT Document | `privacy.py`, `integrity.py` | `test_pdf_extraction_and_redaction` | ✅ PASS |
| **E2E-03** | Handling Corrupt, Empty, or Oversized Documents | `privacy.py`, `app.py` | `test_corrupt_pdf_handling`, `test_empty_document_handling` | ✅ PASS |
| **E2E-04** | Detecting Sensitive Entities Across 6 Classes | `privacy.py` | `test_email_and_phone_detection`, `test_credit_card_and_ssn_detection` | ✅ PASS |
| **E2E-05** | Human-in-the-Loop Redaction Sign-Off & Locking | `app.py`, `privacy.py` | `test_selective_redaction` | ✅ PASS |
| **E2E-06** | Mocked Model Isolation & Prompt Inspection | `document_qa.py` | `test_privacy_gate_model_isolation`, `test_redaction_strictly_precedes_model_request_payload` | ✅ PASS |
| **E2E-07** | Asking Questions Supported by Document Evidence | `document_qa.py` | `test_evidence_grounded_answer` | ✅ PASS |
| **E2E-08** | Verifying Citations Point to Real Pages & Chunks | `document_qa.py` | `test_chunking_preserves_page_metadata` | ✅ PASS |
| **E2E-09** | Rejecting Unsupported Questions (Hallucination Defense) | `document_qa.py` | `test_insufficient_evidence_rejection` | ✅ PASS |
| **E2E-10** | Cryptographic SHA-256 Match on Unchanged Files | `integrity.py` | `test_register_and_verify_match` | ✅ PASS |
| **E2E-11** | Tamper Detection on Single-Byte Modified Files | `integrity.py` | `test_tamper_detection` | ✅ PASS |
| **E2E-12** | Audit Trail Log Sanitization (Zero Secrets in Logs) | `audit.py` | `test_audit_log_never_logs_unredacted_sensitive_data`, `test_audit_logs_never_expose_raw_secrets` | ✅ PASS |
| **E2E-13** | Session State & Document Replacement Reset | `app.py`, `document_qa.py` | `test_document_replacement_clears_stale_index_and_citations` | ✅ PASS |

---

## 3. Detailed Workflow Procedures & Expected Behaviors

### E2E-01: Application Startup & Config Validation
- **Objective**: Verify that TrustLens starts cleanly in localhost-only mode (`127.0.0.1:8501`) and validates environment parameters.
- **Procedure**:
  ```bash
  .venv/bin/streamlit run app.py --server.headless true --server.address 127.0.0.1 --server.port 8501
  curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8501/healthz
  ```
- **Expected Outcome**: Streamlit logs `Uvicorn server started on 127.0.0.1:8501`. HTTP request returns `200`. Zero public `0.0.0.0` ports exposed.
- **Actual Result**: Verified on LinuxONE (`148.100.77.3`) with HTTP 200 response.

---

### E2E-02: Uploading a Valid Synthetic Document
- **Objective**: Ingest multi-page synthetic PDF document (`sample_docs/synthetic_financial_audit_2026.pdf`).
- **Procedure**: Upload file via UI or click `"📄 Load Synthetic Financial Audit"`.
- **Expected Outcome**: Document parsed into 2 distinct pages without text corruption; SHA-256 computed; audit event `DOCUMENT_INGESTED` recorded.
- **Actual Result**: Verified. Digest `1c676404f87e...` calculated over 2,376 bytes.

---

### E2E-03: Handling Invalid, Corrupt, or Empty Documents
- **Objective**: Ensure pipeline gracefully handles zero-byte files, non-PDF formats, and corrupted binary streams.
- **Procedure**: Run `test_corrupt_pdf_handling`, `test_empty_document_handling`, and `test_file_size_limit_validation`.
- **Expected Outcome**: Raises descriptive `ValueError` or user-facing error notification; never crashes or leaks stack trace containing secrets.
- **Actual Result**: 100% passed in automated test suite.

---

### E2E-04: Sensitive Entity Scanning Across 6 Classes
- **Objective**: Scan document text for Emails, Phone Numbers, SSNs, Credit Cards, API Keys, and IP Addresses.
- **Procedure**: Run `PrivacyScanner.scan(pages)`.
- **Expected Outcome**: Detects all 7 synthetic PII items; generates masked previews (`c***@trustlens.internal`, `4***-****-****-1111`) for safe UI inspection.
- **Actual Result**: 7/7 entities detected in synthetic audit document.

---

### E2E-05: Human-in-the-Loop Redaction Sign-Off & Locking
- **Objective**: Auditor selects findings to mask and commits redactions to lock the document representation.
- **Procedure**: In UI, review table, select checkboxes, click `"🔒 Approve Redactions & Lock for AI Processing"`.
- **Expected Outcome**: State switches to `privacy_locked = True`. In-memory text replaces raw PII with `[REDACTED_TYPE_N]` tokens. Raw text is permanently isolated.
- **Actual Result**: Verified in `test_selective_redaction` and live UI.

---

### E2E-06: Mocked Model Isolation & Prompt Inspection
- **Objective**: Prove that raw sensitive values NEVER reach model prompt payloads.
- **Procedure**: Configure pluggable model invoker capturing exact transmitted string. Query model on approved document.
- **Expected Outcome**: 100% of raw sensitive PII strings are absent from the prompt. Evidence context is enclosed inside `<untrusted_document_context>`.
- **Actual Result**: Verified in `test_redaction_strictly_precedes_model_request_payload`.

---

### E2E-07: Grounded Q&A with Physical Page Citations
- **Objective**: Ask question supported by evidence and verify accurate factual retrieval.
- **Procedure**: Submit query: `"What is the total consulting budget?"`.
- **Expected Outcome**: Retrieves Chunk 1 from Page 1; synthesizes answer citing `$4,850,000`; returns citation `Page 1 (CHUNK-001)`.
- **Actual Result**: Verified live in `scripts/verify_linuxone.py`.

---

### E2E-08: Verifying Citation Integrity & Page Metadata
- **Objective**: Confirm that citations point to genuine physical pages rather than arbitrary chunk offsets.
- **Procedure**: Run `test_chunking_preserves_page_metadata`.
- **Expected Outcome**: Chunk objects maintain `page: 1` or `page: 2`. Text never spans across page boundaries.
- **Actual Result**: Verified. Chunk metadata strictly preserved.

---

### E2E-09: Insufficient-Evidence Handling (Zero Hallucination)
- **Objective**: Submit an out-of-scope query lacking document evidence.
- **Procedure**: Submit query: `"What was the CEO's favorite childhood book?"`.
- **Expected Outcome**: Substantive token overlap fails relevance threshold; system explicitly refuses to hallucinate: `"The document does not contain sufficient verifiable evidence to answer this question."`. Citations list is empty.
- **Actual Result**: Verified in `test_insufficient_evidence_rejection`.

---

### E2E-10: SHA-256 Matching on Unchanged Files
- **Objective**: Confirm that an unmodified document matches the registered baseline ledger record.
- **Procedure**: Compute SHA-256 of `synthetic_financial_audit_2026.pdf` and check against reference `DOC-AUDIT-2026`.
- **Expected Outcome**: Status returns `MATCH`, displaying `Zero modifications detected`.
- **Actual Result**: Verified in `test_register_and_verify_match`.

---

### E2E-11: Tamper Detection on Altered Files
- **Objective**: Verify that modifying even one byte in a document triggers a security alert.
- **Procedure**: Compute SHA-256 of `synthetic_tampered_financial_audit.pdf` and verify against reference `DOC-AUDIT-2026`.
- **Expected Outcome**: Status returns `MODIFIED`, triggering `🚨 SECURITY ALERT: The file hash differs from the registered reference.`
- **Actual Result**: Verified in `test_tamper_detection`.

---

### E2E-12: Audit Trail Log Sanitization
- **Objective**: Ensure persistent audit logs never store raw document content or unredacted secrets.
- **Procedure**: Inspect `data/audit_log.json` after running full ingestion, scan, redaction, and query lifecycle.
- **Expected Outcome**: Only counts, hashes, categories, and latencies are recorded. Not a single raw secret appears in the file.
- **Actual Result**: Verified in `test_audit_logs_never_expose_raw_secrets`.

---

### E2E-13: Document Replacement & State Isolation Reset
- **Objective**: Uploading Document B must wipe previous Document A citations and verification status.
- **Procedure**: Load Document A, execute query, upload Document B, query Document A question.
- **Expected Outcome**: Query against Document B returns insufficient evidence; `last_verification` is reset to None; stale citations are eliminated.
- **Actual Result**: Verified in `test_document_replacement_clears_stale_index_and_citations`.
