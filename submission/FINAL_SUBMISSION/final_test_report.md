# TrustLens: Final Test Report & Verification Matrix
**Competition:** IBM Z Datathon 2026  
**Theme:** AI Secured: Innovation Without Exposure  
**Target Environment:** IBM LinuxONE (`s390x`) Community Cloud VM & Windows Workstation  
**Audit Date:** October 2026  
**Overall Result:** 32/32 Tests PASSED (Local) | 32/32 Tests PASSED (LinuxONE) | Deep E2E Verification PASSED  

---

## 1. Local Windows Environment Test Results

- **Environment**: Windows 11, Python 3.11.17 (`win32`), pytest-9.1.1
- **Command Executed**: `.venv\Scripts\python.exe -m pytest tests -v`
- **Total Duration**: 1.79s
- **Pass Rate**: 32/32 (100%)

| Test ID | Feature Tested | Command / Procedure | Result | Evidence / Log Path | Required Follow-up |
|---|---|---|---|---|---|
| **LOC-01** | Page-Preserving Chunking | `pytest tests/test_document_qa.py::test_chunking_preserves_page_metadata` | **PASS** | `tests/test_document_qa.py:46` | None. Page metadata preserved. |
| **LOC-02** | Evidence-Grounded Answer | `pytest tests/test_document_qa.py::test_evidence_grounded_answer` | **PASS** | `tests/test_document_qa.py:72` | None. Factual answer generated. |
| **LOC-03** | Insufficient Evidence Rejection | `pytest tests/test_document_qa.py::test_insufficient_evidence_rejection` | **PASS** | `tests/test_document_qa.py:100` | None. Hallucination blocked. |
| **LOC-04** | Privacy Gate Model Isolation | `pytest tests/test_document_qa.py::test_privacy_gate_model_isolation` | **PASS** | `tests/test_document_qa.py:126` | None. Raw PII absent from chunks. |
| **LOC-05** | Mocked Model Payload Inspection | `pytest tests/test_document_qa.py::test_mocked_model_prompt_payload_inspection` | **PASS** | `tests/test_document_qa.py:155` | None. PII blocked from prompt. |
| **LOC-06** | Prompt Injection Defense | `pytest tests/test_document_qa.py::test_untrusted_document_prompt_injection_defense` | **PASS** | `tests/test_document_qa.py:182` | None. Delimited in XML tags. |
| **LOC-07** | SHA-256 Calculation | `pytest tests/test_integrity.py::test_sha256_calculation` | **PASS** | `tests/test_integrity.py:16` | None. Correct digest returned. |
| **LOC-08** | SHA-256 Empty Bytes | `pytest tests/test_integrity.py::test_sha256_empty_bytes` | **PASS** | `tests/test_integrity.py:27` | None. Returns e3b0c44298fc... |
| **LOC-09** | Reference Registration & Match | `pytest tests/test_integrity.py::test_register_and_verify_match` | **PASS** | `tests/test_integrity.py:35` | None. Ledger persists match. |
| **LOC-10** | Tamper Detection Alert | `pytest tests/test_integrity.py::test_tamper_detection` | **PASS** | `tests/test_integrity.py:53` | None. Single-byte modification caught. |
| **LOC-11** | Unregistered Document Check | `pytest tests/test_integrity.py::test_not_registered_document` | **PASS** | `tests/test_integrity.py:71` | None. Flags NOT_REGISTERED. |
| **LOC-12** | Email & Phone Detection | `pytest tests/test_privacy.py::test_email_and_phone_detection` | **PASS** | `tests/test_privacy.py:16` | None. Regex matches formats. |
| **LOC-13** | Card & SSN Detection | `pytest tests/test_privacy.py::test_credit_card_and_ssn_detection` | **PASS** | `tests/test_privacy.py:35` | None. Matches 16-digit cards & SSNs. |
| **LOC-14** | Redaction Behavior | `pytest tests/test_privacy.py::test_redaction_behavior` | **PASS** | `tests/test_privacy.py:54` | None. Tokens replace raw text. |
| **LOC-15** | Selective Redaction Sign-Off | `pytest tests/test_privacy.py::test_selective_redaction` | **PASS** | `tests/test_privacy.py:75` | None. User selection honored. |
| **LOC-16** | PDF Extraction & Redaction | `pytest tests/test_privacy.py::test_pdf_extraction_and_redaction` | **PASS** | `tests/test_privacy.py:97` | None. Native PDF parsing works. |
| **LOC-17** | Pre-Prompt Model Quarantine | `pytest tests/test_privacy_boundaries.py::test_redaction_strictly_precedes_model_request_payload` | **PASS** | `tests/test_privacy_boundaries.py:50` | None. Zero sensitive PII in prompt. |
| **LOC-18** | Unapproved Query Rejection | `pytest tests/test_privacy_boundaries.py::test_unapproved_document_cannot_be_queried` | **PASS** | `tests/test_privacy_boundaries.py:94` | None. Rejects unindexed state. |
| **LOC-19** | Untrusted Context Defense | `pytest tests/test_privacy_boundaries.py::test_prompt_injection_defense_in_model_payload` | **PASS** | `tests/test_privacy_boundaries.py:105` | None. XML framing confirmed. |
| **LOC-20** | Audit Log Secret Sanitization | `pytest tests/test_privacy_boundaries.py::test_audit_logs_never_expose_raw_secrets` | **PASS** | `tests/test_privacy_boundaries.py:134` | None. Zero secrets in audit logs. |
| **LOC-21** | Document Replacement Reset | `pytest tests/test_privacy_boundaries.py::test_document_replacement_clears_stale_index_and_citations` | **PASS** | `tests/test_privacy_boundaries.py:175` | None. Wipes stale chunks. |
| **LOC-22** | RBAC Role Definitions | `pytest tests/test_rbac.py::test_role_definitions_exist` | **PASS** | `tests/test_rbac.py:12` | None. 3 roles defined. |
| **LOC-23** | Security Officer Permissions | `pytest tests/test_rbac.py::test_security_officer_permissions` | **PASS** | `tests/test_rbac.py:19` | None. Full admin privileges. |
| **LOC-24** | Compliance Auditor Permissions | `pytest tests/test_rbac.py::test_compliance_auditor_permissions` | **PASS** | `tests/test_rbac.py:27` | None. Read-only audit rights. |
| **LOC-25** | Restricted Viewer Permissions | `pytest tests/test_rbac.py::test_restricted_viewer_permissions` | **PASS** | `tests/test_rbac.py:35` | None. Uploads blocked. |
| **LOC-26** | Sensitive Value UI Masking | `pytest tests/test_security_edge_cases.py::test_sensitive_value_masking` | **PASS** | `tests/test_security_edge_cases.py:15` | None. Masks preview strings. |
| **LOC-27** | Corrupt PDF Error Handling | `pytest tests/test_security_edge_cases.py::test_corrupt_pdf_handling` | **PASS** | `tests/test_security_edge_cases.py:28` | None. Graceful error handling. |
| **LOC-28** | Empty Document Handling | `pytest tests/test_security_edge_cases.py::test_empty_document_handling` | **PASS** | `tests/test_security_edge_cases.py:36` | None. Graceful error handling. |
| **LOC-29** | Custom Sensitive Pattern | `pytest tests/test_security_edge_cases.py::test_custom_sensitive_pattern` | **PASS** | `tests/test_security_edge_cases.py:44` | None. Pluggable pattern scanner. |
| **LOC-30** | File Size Limit Enforcement | `pytest tests/test_security_edge_cases.py::test_file_size_limit_validation` | **PASS** | `tests/test_security_edge_cases.py:60` | None. Rejects files > 20 MB. |
| **LOC-31** | Unredacted PII Audit Masking | `pytest tests/test_security_edge_cases.py::test_audit_log_never_logs_unredacted_sensitive_data` | **PASS** | `tests/test_security_edge_cases.py:68` | None. Logs counts and hashes only. |
| **LOC-32** | Corrupt Ledger Recovery | `pytest tests/test_security_edge_cases.py::test_corrupted_integrity_ledger_graceful_recovery` | **PASS** | `tests/test_security_edge_cases.py:91` | None. Self-healing JSON ledger. |

---

## 2. IBM LinuxONE Remote Mainframe (`s390x`) Test Results

- **Environment**: Ubuntu 24.04.5 LTS (`s390x`), Python 3.12.3, 3 vCPUs, 8 GB RAM
- **Host Public IP**: `148.100.77.3`
- **Command Executed**: `/home/linux1/TrustLens/.venv/bin/pytest tests/ -v`
- **Total Duration**: 0.29s
- **Pass Rate**: 32/32 (100%)

| Test ID | Feature Tested | Remote LinuxONE Command | Result | Evidence Observed |
|---|---|---|---|---|
| **LONE-01** | Full Automated Test Suite (32 tests) | `/home/linux1/TrustLens/.venv/bin/pytest tests/ -v` | **PASS** | `32 passed in 0.29s` on native s390x CPU. |
| **LONE-02** | Deep Verification Script | `/home/linux1/TrustLens/.venv/bin/python3 scripts/verify_linuxone.py` | **PASS** | All 4 gates passed; live SHA-256 match, tamper alert, 7/7 PII masked, grounded Q&A verified. |
| **LONE-03** | Streamlit Service Health Check | `curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8501/healthz` | **PASS** | HTTP Status `200` (OK). |
| **LONE-04** | Streamlit Root Application Page | `curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8501/` | **PASS** | HTTP Status `200` (OK). |
| **LONE-05** | Localhost Network Isolation | `netstat -tlpn \| grep 8501` | **PASS** | Strictly bound to `127.0.0.1:8501`. Zero public internet exposure. |
| **LONE-06** | SSH Port Forwarding Access | `ssh -L 8501:127.0.0.1:8501 linux1@148.100.77.3` | **PASS** | Secure bidirectional encrypted tunnel verified from local browser. |

---

## 3. Tests Not Yet Executed (Human Submission Prerequisites)

| Item | Action Required by Human Submitter | Target Deliverable | Status |
|---|---|---|---|
| **MAN-01** | Record 3-minute video presentation | Follow [submission/demo_script.md](file:///d:/IBM_IDEATHON/submission/demo_script.md) & [submission/demo_rehearsal.md](file:///d:/IBM_IDEATHON/submission/demo_rehearsal.md) | ⏳ Awaiting Recording |
| **MAN-02** | Upload video & insert URL | YouTube / Vimeo link into `submission/form_answers.md` Field 7 | ⏳ Awaiting Link |
| **MAN-03** | Push codebase to public GitHub | Push `git` repository and insert URL into `submission/form_answers.md` Field 6 | ⏳ Awaiting Push |
| **MAN-04** | Submit official Datathon form | Copy verified answers from `submission/form_answers.md` into IBM submission portal | ⏳ Awaiting Submission |

---

## 4. Files Modified During Prompt 6 Testing

1. `config.py`:
   - Enhanced `EMAIL` regex pattern to support modern gTLDs with up to 24 characters (`{2,24}`), reliably capturing enterprise domains like `.internal`.
   - Enhanced `CREDIT_CARD` regex pattern to support hyphenated and spaced 16-digit card numbers (`4111-2222-3333-4444`).
2. `app.py`:
   - Enhanced `process_uploaded_file`: guaranteed that uploading a new document immediately wipes stale verification results (`last_verification = None`), clears prior chunk indexes (`qa_pipeline = DocumentQAPipeline()`), and resets redaction summaries.
3. `tests/test_privacy_boundaries.py`:
   - Created dedicated regression suite testing model payload quarantine, prompt injection defense, audit log sanitization, and document replacement state resets.
4. `submission/e2e_test_plan.md`:
   - Created formal 13-workflow test plan with procedures, expected outputs, and pass criteria.
5. `submission/demo_rehearsal.md`:
   - Created operator rehearsal guide with exact UI clicks, inputs, expected visible banners, and fallback contingency steps.
6. `dist/trustlens_s390x_deploy.tar.gz`:
   - Re-packaged clean, verified distribution archive bundling updated code, tests, and submission assets (100.86 KB, SHA-256 `2F1A32D743758DEB405A2BDAF1E0211ED0B564828C454AE1F0CB053EF431CFCB`).

---

## 5. Remaining High-Priority Risks & Operational Guidance

- **Public Network Binding**: Always run Streamlit bound to `127.0.0.1`. Never bind to `0.0.0.0` on IBM LinuxONE Community Cloud instances unless behind an enterprise reverse proxy with TLS and authentication.
- **SSH Private Key Confidentiality**: Keep `trustlenskey.pem` secure in your local Downloads folder. Never push it to GitHub or share it.
- **Cryptographic Scope**: SHA-256 proves byte-level document consistency relative to reference baseline records; it does not attest to human legal authorship.

---

## 6. Exact Command to Start TrustLens on LinuxONE

In Windows PowerShell, launch the secure SSH tunnel:
```powershell
ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3
```

Inside that remote session, start the application:
```bash
cd ~/trustlens
.venv/bin/streamlit run app.py --server.headless true --server.address 127.0.0.1 --server.port 8501
```

Access the dashboard in your local browser at:
```text
http://localhost:8501
```
