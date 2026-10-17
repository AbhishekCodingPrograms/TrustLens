# TrustLens: Final Hackathon Audit & Verification Report
**Competition:** IBM Z Datathon 2026  
**Theme:** AI Secured: Innovation Without Exposure  
**Track:** Document Intelligence & Enterprise Mainframe Security  
**Audit Date:** October 2026  
**Evaluation Status:** 100% Passed (All Local & Remote Verification Tests)  

---

## 1. Executive Summary

This report documents the final software, security, deployment, and evidence audit for **TrustLens: Privacy-Gated AI with Verifiable Evidence**. All tests, remote mainframe commands, and security validations recorded below were executed and observed directly on a Windows development workstation and an IBM LinuxONE Community Cloud virtual server (`s390x`).

| Dimension | Verification Method | Result | Evidence Status |
|---|---|---|---|
| **Local Unit & Security Tests** | `pytest tests/ -v` (Windows) | 27/27 PASSED (1.87s) | ✅ Verified |
| **LinuxONE Native Tests** | `pytest tests/ -v` (`s390x` VM) | 27/27 PASSED (0.26s) | ✅ Verified |
| **Deep Verification Pipeline** | `verify_linuxone.py` (`s390x`) | All 4 Gates PASSED (0.18s) | ✅ Verified |
| **Streamlit Web Application** | HTTP health check on `127.0.0.1:8501` | HTTP Status `200` (OK) | ✅ Verified |
| **Encrypted Access Path** | SSH Port Forwarding (`-L 8501...`) | Port 8501 tunnel verified | ✅ Verified |
| **Secret & Cache Sanitization** | Cryptographic scan before tar | 0 secrets / 0 caches | ✅ Verified |
| **Clean Deployment Package** | `dist/trustlens_s390x_deploy.tar.gz` | SHA-256 verified | ✅ Verified |
| **Pitch Deck Deliverable** | `submission/trustlens_pitch_deck.pdf` | 15.25 KB (< 5 MB limit) | ✅ Verified |

---

## 2. Files Inspected and Modified

### Source Code Inspected
- `app.py`: Streamlit multi-page interface, session state managers, and role-based access control UI gating.
- `document_qa.py`: Page-preserving chunker, BM25 retrieval engine, `<untrusted_document_context>` XML delimiters, and system prompt anti-injection guardrails.
- `privacy.py`: Multi-pattern regex scanner, safe preview masking, and in-memory redaction engine.
- `integrity.py`: SHA-256 calculation, atomic baseline ledger registration, and modification detection.
- `audit.py`: Append-only JSON audit logging and operational metric calculations.
- `config.py`: Port numbers, default model definitions, relevance thresholds, and 3-tier RBAC permission definitions.

### Files Created or Updated for Submission
- `submission/architecture_diagram.mmd`: Editable Mermaid architecture diagram distinguishing tested components, external services, and future roadmaps.
- `submission/architecture_diagram.html`: High-resolution vector rendered diagram viewable in any standard browser.
- `submission/demo_script.md`: Timed 3-minute presentation script (0:00–3:00) with spoken narrative, screen actions, and fallback contingency plans.
- `submission/pitch_deck.md`: 9-slide markdown presentation source.
- `submission/trustlens_pitch_deck.pdf`: 9-slide landscape corporate PDF presentation (15.25 KB).
- `submission/form_answers.md`: Form answers for all 10 hackathon submission fields, strictly constrained under 1024 characters each.
- `scripts/verify_linuxone.py`: End-to-end deep verification script testing real sample PDFs.
- `scripts/package_for_linuxone.ps1`: Packaging automation script bundling source code, sample documents, tests, scripts, and submission deliverables.
- `dist/trustlens_s390x_deploy.tar.gz`: Clean deployment archive.

---

## 3. Automated Test Execution & Observed Results

### 3.1 Local Development Workstation (Windows 11, Python 3.11.17)
```powershell
.venv\Scripts\python.exe -m pytest tests -v
```
**Outcome: 27 passed in 1.87s**
- Document QA chunking & metadata preservation: PASSED
- Evidence-grounded answers & citations: PASSED
- Insufficient evidence rejection: PASSED
- Privacy gate model isolation: PASSED
- Mocked model prompt payload inspection: PASSED
- Untrusted document prompt injection defense: PASSED
- SHA-256 calculation & empty bytes: PASSED
- Integrity match & tamper detection: PASSED
- Sensitive entity detection (Emails, Phones, Cards, SSNs): PASSED
- In-memory redaction & selective masking: PASSED
- RBAC permissions (Security Officer, Auditor, Viewer): PASSED
- Security edge cases (corrupt files, limits, audit log masking): PASSED

### 3.2 IBM LinuxONE Mainframe (`s390x`, Python 3.12.3)
```bash
/home/linux1/TrustLens/.venv/bin/pytest tests/ -v
```
**Outcome: 27 passed in 0.26s natively on s390x CPU**
- Full test suite passed without modification or platform warning on Ubuntu 24.04.5 LTS.

### 3.3 Deep End-to-End Verification Run on LinuxONE
```bash
/home/linux1/TrustLens/.venv/bin/python3 scripts/verify_linuxone.py
```
**Verified Pipeline Stages:**
1. *SHA-256 Integrity Gate*: Registered baseline hash `1c676404f87e...`. Original verified as `MATCH`. Tampered document instantly flagged as `MODIFIED` (`[PASSED]`).
2. *Privacy Gate & Masking*: 7 sensitive items detected across 4 categories (`CREDIT_CARD`, `EMAIL`, `IP_ADDRESS`, `PHONE_NUMBER`). 100% of sensitive strings masked from redacted context (`[PASSED]`).
3. *Grounded QA & Isolation*: Query answered with verified citation `Page 1 (CHUNK-001)`. Captured model prompt payload verified to contain `<untrusted_document_context>` and zero sensitive PII strings (`[PASSED]`).
4. *Hallucination Rejection*: Out-of-scope query rejected with `"The document does not contain sufficient verifiable evidence"` (`[PASSED]`).
5. *Tamper-Evident Audit Trail*: All lifecycle events recorded; real dashboard metrics computed with average latency of 10.3 ms (`[PASSED]`).

---

## 4. Verified Security Controls & Honest Limitations

### Verified Security Controls
- **Zero Raw Document Exposure**: The vector indexing and LLM prompt generation modules accept only text where `privacy_approved` is confirmed. Raw text cannot bypass this barrier.
- **Safe Review Previews**: Auditor tables mask sensitive values (`j***@trustlens.internal`, `4***-****-****-1111`) so humans reviewing findings do not cause shoulder-surfing or UI leaks.
- **Prompt Injection Containment**: Ingested document content is wrapped in `<untrusted_document_context>` tags with explicit system directives prohibiting the execution of embedded instructions.
- **Grounded Citation Verifiability**: Page citations map strictly to the physical document pages where evidence originated.
- **Localhost Hardening**: Server binds to `127.0.0.1:8501`. Network scanning from the public internet finds no open application ports.

### Remaining System Limitations (Honest Disclaimers)
- **Regex Coverage Limits**: Regular expressions catch standard structured PII reliably. Highly unstructured or contextual PII (e.g. non-standard human names) requires human auditor confirmation.
- **Demonstration RBAC**: Role-based access control in `app.py` enforces session-level separation of duties. Enterprise deployments will federate with IBM RACF, LDAP, or SAML SSO.
- **Cryptographic Scope**: SHA-256 hashes detect byte-level file modifications relative to a baseline; they prove consistency with a reference, not legal human authorship or creation timestamps.
- **No Unverified Claims**: We make zero claims regarding quantum-safe cryptography, hardware security modules, or IBM AI accelerators.

---

## 5. LinuxONE Mainframe Hardware Telemetry

Measured live on remote instance `148.100.77.3`:
- **Architecture**: `s390x` (IBM zArchitecture, `z13` baseline with `z16` tuning flags `-mzarch -mtune=z16`)
- **Host OS**: Ubuntu 24.04.5 LTS (`noble`), Kernel 6.8.0-147-generic
- **Compute Resources**: 3 vCPUs, 8 GB RAM, 50 GB disk
- **Disk Utilization**: `/dev/dasda1` direct-access storage device has 3.8 GB used, 44 GB available (8% utilization)
- **Memory Utilization**: 1304 MB used, 6704 MB available
- **Pytest Suite Runtime**: 0.26 seconds for 27 tests
- **Deep Pipeline Runtime**: 0.18 seconds end-to-end
- **Streamlit Localhost Response**: HTTP 200 OK on `http://127.0.0.1:8501/healthz`

---

## 6. Architecture-Specific Dependency Resolution

During remote LinuxONE deployment, compiling C/Rust extensions (`numpy`, `pandas`, `pyarrow`, `libcst`) from source on `s390x` presented compilation bottlenecks.

**Engineering Resolution Applied:**
1. Installed Canonical's pre-compiled Ubuntu noble `s390x` binary packages:
   ```bash
   sudo apt-get install -y python3-numpy python3-pandas python3-libcst
   ```
2. Initialized the virtual environment with `--system-site-packages`:
   ```bash
   python3 -m venv --system-site-packages .venv
   ```
3. Installed pure-Python dependencies (`pypdf`, `fpdf2`, `pytest`, `python-dotenv`, `streamlit --no-deps`) directly as universal wheels.
4. Result: Zero source compilation required; virtual environment setup completes in seconds with 100% native execution speed.

---

## 7. Submission Artifact Locations

| Artifact | File Location | Verified Properties |
|---|---|---|
| **Clean Source Archive** | `dist/trustlens_s390x_deploy.tar.gz` | Clean tarball, zero secrets, verified SHA-256 |
| **Pitch Deck Presentation** | `submission/trustlens_pitch_deck.pdf` | 15.25 KB, 9 landscape slides, well under 5 MB |
| **Pitch Deck Markdown** | `submission/pitch_deck.md` | Complete 9-slide markdown script |
| **Architecture Diagram (Source)**| `submission/architecture_diagram.mmd` | Editable Mermaid flowchart |
| **Architecture Diagram (HTML)** | `submission/architecture_diagram.html` | High-res browser-viewable vector diagram |
| **Video Walkthrough Script** | `submission/demo_script.md` | Timed 3:00 script with screen actions and fallbacks |
| **Submission Form Answers** | `submission/form_answers.md` | Draft answers for all 10 form fields (< 1024 chars) |
| **Verification & Test Report** | `docs/verification_report.md` | Complete test logs and LinuxONE telemetry |

---

## 8. Remaining Actions Required Before Form Submission

1. **Push Source Code to GitHub**:
   - Initialize git (if not already done) and push your project to a public repository.
   - Insert the public GitHub URL into **Field 6** of `submission/form_answers.md`.
2. **Record 3-Minute Demonstration Video**:
   - Open TrustLens via SSH tunnel (`ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3`).
   - Follow the step-by-step narrative and screen actions in `submission/demo_script.md`.
   - Upload the video to YouTube, Vimeo, or an unlisted cloud drive.
   - Insert the video link into **Field 7** of `submission/form_answers.md`.
3. **Submit the Datathon Form**:
   - Copy and paste the pre-verified answers from `submission/form_answers.md` directly into the IBM Z Datathon 2026 submission form.
   - Attach `submission/trustlens_pitch_deck.pdf` as your slide deck.
