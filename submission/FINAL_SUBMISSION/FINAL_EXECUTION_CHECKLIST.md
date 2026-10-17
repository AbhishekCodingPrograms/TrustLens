# TrustLens: Final Demo Recording & Submission Execution Checklist

**Competition:** IBM Z Datathon 2026  
**Track:** AI Secured: Innovation Without Exposure  
**Platform:** IBM LinuxONE Community Cloud (Ubuntu 24.04.5 LTS, `s390x`, `148.100.77.3`)  
**Release Version:** v1.0.0-final  
**Release Date:** October 18, 2026  

---

## 1. Final Verification Results (PASS / FAIL / BLOCKED / NOT RUN)

All functional, security, and deployment checks have been verified with live execution results:

| Verification Item | Target Environment | Verification Command / Evidence | Status | Verified Outcome |
| :--- | :--- | :--- | :---: | :--- |
| **Streamlit Application Startup** | LinuxONE `s390x` | `curl -sI http://127.0.0.1:8501/_stcore/health` | **PASS** | `HTTP/1.1 200 OK`; active under PID `12799` bound to `127.0.0.1:8501`. |
| **Sensitive Data Detection** | Local & LinuxONE | `PrivacyScanner.scan()` | **PASS** | Detects 7 sensitive values across 4 types (`CREDIT_CARD`, `EMAIL`, `PHONE_NUMBER`, `IP_ADDRESS`). |
| **Sensitive Value Redaction** | Local & LinuxONE | `PrivacyScanner.redact_text_pages()` | **PASS** | 7 redactions applied; zero raw sensitive values remain in redacted text. |
| **Model Payload Isolation** | LinuxONE `s390x` | `pytest tests/test_privacy_boundaries.py` | **PASS** | Outgoing model prompt contains 0 unmasked strings; wrapped in `<untrusted_document_context>`. |
| **Evidence-Grounded Citations** | LinuxONE `s390x` | `scripts/validate_user_journey.py` | **PASS** | Returns physical page citations: `Page 1 (CHUNK-001)` and `Page 2 (CHUNK-002)`. |
| **Hallucination Refusal Fallback** | LinuxONE `s390x` | `scripts/validate_user_journey.py` | **PASS** | Unsupported inquiry cleanly rejected without hallucinating facts. |
| **SHA-256 Match (Original)** | LinuxONE `s390x` | `IntegrityManager.verify_file()` | **PASS** | Status: `MATCH` (Baseline hash `1c676404...` matches byte-for-byte). |
| **SHA-256 Tamper Detection** | LinuxONE `s390x` | `IntegrityManager.verify_file()` | **PASS** | Status: `MODIFIED` (Cryptographic warning triggered on tampered document). |
| **Automated Test Suite (32 tests)**| LinuxONE `s390x` | `.venv/bin/pytest tests/ -q` | **PASS** | **32 / 32 passed in 0.28s** natively on `s390x` CPU. |
| **Complete 11-Step User Journey** | LinuxONE `s390x` | `.venv/bin/python3 scripts/validate_user_journey.py`| **PASS** | **11 / 11 steps passed** natively on LinuxONE. |
| **Release Archive CRC Integrity** | Workspace | `zipfile.testzip()` | **PASS** | 56 files, 0 CRC errors, 171.56 KB, zero `.env` or keys. |
| **Pitch Deck PDF Compliance** | Workspace | `pypdf.PdfReader()` | **PASS** | 9 slides, 15.25 KB, opens cleanly (< 5 MB limit). |
| **Portal Form Answers (10 fields)**| Workspace | `scripts/verify_form_answers.py` | **PASS** | All 10 fields confirmed strictly <= 1024 characters. |
| **Public GitHub Repository Link** | Competition Portal | Field 6 in portal | **PENDING** | Marked pending human repository push to personal GitHub. |
| **Video Demonstration URL** | Competition Portal | Field 7 in portal | **PENDING** | Marked pending human 3-minute video recording and upload. |

---

## 2. Completed Tasks vs. Missing Tasks

### Completed Tasks (100% Finished):
- [x] Full source code implementation (`app.py`, `privacy.py`, `integrity.py`, `document_qa.py`, `audit.py`, `config.py`).
- [x] Complete 32-test automated regression suite passing locally and on LinuxONE.
- [x] Defense-in-depth Privacy Gate enforcing programmatic blocking before model prompt construction.
- [x] Cryptographic SHA-256 tamper-evident integrity tracking.
- [x] Verified deployment to IBM LinuxONE Community Cloud (`148.100.77.3`, `s390x`), active on port 8501.
- [x] Verified release ZIP package ([trustlens_release.zip](file:///d:/IBM_IDEATHON/submission/FINAL_SUBMISSION/trustlens_release.zip)).
- [x] Verified 9-slide Pitch Deck PDF under 5 MB ([trustlens_pitch_deck.pdf](file:///d:/IBM_IDEATHON/submission/FINAL_SUBMISSION/trustlens_pitch_deck.pdf)).
- [x] Verified 180-second demo script and recording checklist ([demo_rehearsal.md](file:///d:/IBM_IDEATHON/submission/FINAL_SUBMISSION/demo_rehearsal.md)).
- [x] Copy-ready submission form answers adhering to 1024-char limits ([COPY_PASTE_ANSWERS.md](file:///d:/IBM_IDEATHON/submission/FINAL_SUBMISSION/COPY_PASTE_ANSWERS.md)).

### Missing Tasks (2 User Actions Required):
- [ ] **Action 1:** Push the Git repository to your personal public GitHub account and update Field 6.
- [ ] **Action 2:** Record the 3-minute video demo, upload to YouTube/Vimeo/Drive, and update Field 7.

---

## 3. Exact Artifact Paths

| Artifact Deliverable | Absolute File Path | Description |
| :--- | :--- | :--- |
| **Release Archive** | `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\trustlens_release.zip` | 171.56 KB clean submission ZIP |
| **Pitch Deck PDF** | `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\trustlens_pitch_deck.pdf` | 15.25 KB verified 9-slide PDF |
| **Submission Form Answers**| `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\COPY_PASTE_ANSWERS.md` | All 10 competition answers <= 1024 chars |
| **Demo Rehearsal Script** | `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\demo_rehearsal.md` | Minute-by-minute 180s walkthrough |
| **Recording Checklist** | `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\recording_checklist.md` | Step-by-step video recording screen actions |
| **Judge Technical QA** | `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\judge_qa.md` | Rigorous answers to 12 judge questions |
| **Evidence Matrix** | `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\evidence_matrix.md` | 16 claims cross-referenced with code |
| **Architecture Diagram** | `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\architecture_diagram.html` | Vector SVG architecture visualization |

---

## 4. Exact Manual Steps to Record & Upload the Video

### Step 1: Establish Secure SSH Tunnel
Run in **Windows PowerShell**:
```powershell
ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3
```
Keep this PowerShell window open during recording.

### Step 2: Open Browser to Live LinuxONE UI
Open **Chrome or Edge** to `http://localhost:8501`. Have terminal ready in background.

### Step 3: Record 3-Minute Walkthrough (Follow Timed Flow)
- **`0:00 - 0:30` | Problem & Architecture:** Show **Security Dashboard**. State the problem: GenAI exposes PII and hallucinates. TrustLens enforces privacy gating and verifiable evidence before LLM ingestion.
- **`0:30 - 1:05` | Integrity Gate:** Ingest `sample_docs/synthetic_financial_audit_2026.pdf` -> Status shows `MATCH`. Next, verify `sample_docs/synthetic_tampered_financial_audit.pdf` -> Alert triggers `MODIFIED`.
- **`1:05 - 1:45` | Privacy Gate:** Scan document -> 7 sensitive items detected (Email, Phone, Card, IP). Review selective mask toggles, then click **"Approve Redactions & Lock Document"**.
- **`1:45 - 2:25` | Grounded Q&A:** Query: *"What is the settlement or reserve amount?"* -> Returns exact figure with physical citations `Page 1 (CHUNK-001)` and `Page 2 (CHUNK-002)`. Query: *"What was the CEO's favorite childhood book?"* -> Clean refusal without hallucination.
- **`2:25 - 2:45` | IBM LinuxONE Native Proof:** Alt-Tab to SSH terminal, run:
  ```bash
  uname -m; .venv/bin/pytest tests/ -q
  ```
  Shows `s390x` architecture and `32 passed in 0.28s`.
- **`2:45 - 3:00` | Audit Ledger & Wrap Up:** Show tamper-evident operational log and conclude.

### Step 4: Upload Video
Upload to YouTube (set to **Unlisted** or **Public**), Vimeo, or Google Drive (set access to *"Anyone with the link can view"*). Copy the video URL.

---

## 5. Exact Steps to Complete the Datathon Form

1. Open [submission/FINAL_SUBMISSION/COPY_PASTE_ANSWERS.md](file:///d:/IBM_IDEATHON/submission/FINAL_SUBMISSION/COPY_PASTE_ANSWERS.md).
2. Paste your GitHub repository URL into **Field 6**.
3. Paste your video demonstration URL into **Field 7**.
4. Open the IBM Z Datathon submission portal in your browser.
5. Copy and paste Fields 1 through 10 directly into the portal fields.
6. Upload [submission/FINAL_SUBMISSION/trustlens_pitch_deck.pdf](file:///d:/IBM_IDEATHON/submission/FINAL_SUBMISSION/trustlens_pitch_deck.pdf).
7. Submit the form!
