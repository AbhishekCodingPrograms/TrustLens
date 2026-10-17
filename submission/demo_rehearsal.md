# TrustLens: Judge-Ready Live Demo Script & Operator Rehearsal Guide

**Competition:** IBM Z Datathon 2026  
**Track:** AI Secured: Innovation Without Exposure  
**Platform:** IBM LinuxONE Community Cloud (Ubuntu 24.04.5 LTS, `s390x`, IP: `148.100.77.3`)  
**Access Model:** Local Web Browser via SSH Port-Forwarding (`http://localhost:8501`)  
**Target Duration:** Exactly 3 Minutes (180 Seconds)  
**Verification Level:** 100% Verified on Live LinuxONE Hardware  

---

## 1. Quick Operator Checklist (T-minus 3 Minutes)

### Terminal 1: Active SSH Tunnel & Remote Streamlit Service
```powershell
# Establish secure encrypted tunnel to LinuxONE Community Cloud
ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3
```
*Verification Check:* Application is already active under PID `12799` on `127.0.0.1:8501`. If a restart is ever required:
```bash
cd ~/TrustLens
.venv/bin/streamlit run app.py --server.headless true --server.address 127.0.0.1 --server.port 8501
```

### Terminal 2: Mainframe Verification Terminal
Open a second PowerShell window ready to demonstrate live mainframe execution:
```powershell
ssh -i "$HOME\Downloads\trustlenskey.pem" linux1@148.100.77.3
```
*Pre-staged command in history:*
```bash
uname -m && /home/linux1/TrustLens/.venv/bin/pytest /home/linux1/TrustLens/tests/ -q
```

### Browser Configuration
- Navigate to: `http://localhost:8501`
- Confirm Role: **"Security Officer"** (top of sidebar)
- Zoom Level: Set to 100% or 110% for crisp 1080p recording.

---

## 2. Minute-by-Minute Rehearsal Script (180 Seconds)

```
0:00 ─── 0:30  Segment 1: Problem Hook & Security Dashboard
0:30 ─── 1:05  Segment 2: Cryptographic Document Integrity Gate
1:05 ─── 1:45  Segment 3: Privacy Gate & Selective Masking
1:45 ─── 2:25  Segment 4: Evidence-Grounded Q&A & Hallucination Refusal
2:25 ─── 2:45  Segment 5: Live IBM LinuxONE Mainframe Verification
2:45 ─── 3:00  Segment 6: Operational Audit Trail & Closing
```

---

### Segment 1: Problem Hook & Security Dashboard (0:00 – 0:30)

- **Screen Action:** Browser open at `http://localhost:8501` on **"📊 Security Dashboard"**.
- **Spoken Voiceover (Rehearsed):**
  > "Hello judges! Enterprise teams in banking, healthcare, and government are desperate to leverage Generative AI on confidential documents. But doing so creates three massive security risks: leaking sensitive PII and financial secrets into AI models, accepting fabricated hallucinations, and failing to detect unauthorized document tampering.
  >
  > Welcome to **TrustLens: Privacy-Gated AI with Verifiable Evidence**, running live on IBM LinuxONE. TrustLens is a zero-trust document intelligence platform that cryptographically validates file integrity, quarantines sensitive data before it reaches AI models, and provides 100% evidence-grounded answers with exact physical page citations."
- **Visual Cues:** Hover briefly over the dashboard metric cards showing real operational data: *Documents Processed*, *Sensitive Items Detected*, *Integrity Checks*, and *Average Query Latency*.

---

### Segment 2: Cryptographic Document Integrity Gate (0:30 – 1:05)

- **Screen Action 1:** Click **"🔐 Integrity Gate"** in the sidebar.
- **Screen Action 2:** Click the button: **`"📄 Load Synthetic Financial Audit"`** (or upload `sample_docs/synthetic_financial_audit_2026.pdf`).
- **Visible Hash:** Point cursor to the registered SHA-256 fingerprint:  
  `1c676404f87e98a9f13ce75b10a97d3dfcb9cf5b56c5bf24bbcd8546c65ffe84`
- **Screen Action 3:** Click **"🔍 Verify Integrity Against Baseline"**.
- **Expected Visual Output:** Immediate green banner:
  ```text
  ✅ INTEGRITY CHECK PASSED (MATCH)
  File matches registered reference 'DOC-AUDIT-2026'. Zero modifications detected.
  ```
- **Screen Action 4:** In the same tab, click **`"📄 Load Tampered Financial Audit"`** (or upload `sample_docs/synthetic_tampered_financial_audit.pdf`).
- **Screen Action 5:** Click **"🔍 Verify Integrity Against Baseline"**.
- **Expected Visual Output:** Immediate prominent red alert:
  ```text
  🚨 SECURITY ALERT (MODIFIED)
  The file hash differs from the registered reference. The document has been modified or corrupted.
  Expected: 1c676404f87e98a9f13ce75b10a97d3dfcb9cf5b56c5bf24bbcd8546c65ffe84
  Computed: 9f54027d1dba1ef0dce45429400224b5189d7ada80b636e9c06e538eb48118f3
  ```
- **Spoken Voiceover:**
  > "First, the Integrity Gate calculates a SHA-256 digest over the raw bytes before parsing. When we verify our authentic audit document, it matches our reference ledger exactly. But when an unauthorized party alters an escrow disbursement from \$142 Million to \$999 Million, TrustLens immediately catches the byte-level discrepancy and triggers a security alert before any model ingestion occurs."

---

### Segment 3: Privacy Gate & Selective Masking (1:05 – 1:45)

- **Screen Action 1:** Click **"👁️ Privacy Gate & Redaction"** in the sidebar.
- **Screen Action 2:** Re-load **`"📄 Load Synthetic Financial Audit"`**.
- **Visible Inspection:** Point to the findings table showing 7 detected entities across 4 categories:
  - Emails: `m***@continental-reserve.com`, `c***@continental-reserve.com`
  - Credit Card: `4***-****-****-4444`
  - Phone: `+1 (555) ***-8821`
  - Internal Gateway IP: `10.240.12.***`
- **Screen Action 3:** Click **"🔒 Approve Redactions & Lock for AI Processing"**.
- **Expected Visual Output:** Green confirmation:
  ```text
  Applied 7 redactions! Document locked and 2 chunks indexed for Q&A.
  ```
- **Screen Action 4:** Click the sub-tab **"🔒 Approved Redacted Text"** to show that raw values have been converted to tokens like `[REDACTED_CREDIT_CARD_6]` and `[REDACTED_EMAIL_1]`.
- **Screen Action 5:** Click sub-tab **"📄 Original Raw Text"** and highlight the red warning: *"Restricted View: This raw text is strictly BLOCKED from reaching the AI model."*
- **Spoken Voiceover:**
  > "Next is the Privacy Gate. TrustLens scans extracted text across emails, phone numbers, corporate tax IDs, credit cards, and internal IPs, rendering safe masked previews. Once the compliance auditor reviews and approves redactions, the document is locked. Crucially, raw confidential text is completely quarantined in-memory—only the sanitized representation is indexed into our vector search engine."

---

### Segment 4: Evidence-Grounded Q&A & Hallucination Refusal (1:45 – 2:25)

- **Screen Action 1:** Click **"💡 Evidence-Grounded Q&A"** in the sidebar.
- **Visible Confirmation:** Notice the shield banner: *"🔒 Protected AI Pipeline Active"*.
- **Screen Action 2:** Click the sample query button: **`"❓ What is the settlement or reserve amount?"`**.
- **Screen Action 3:** Click **"🔎 Submit Grounded Query"**.
- **Expected Visual Output:**
  - Answer rendered:
    ```text
    Evidence-Grounded Findings:
    • [Page 2]: "Approved Settlement Amount: $142,500,000 USD. Settlement Date: September 28, 2026."
    • [Page 1]: "Continental Reserve Bank maintains total Tier-1 capital reserves of $14.85 Billion USD across institutional vaults."
    ```
  - Citations displayed: `Page 1 (CHUNK-001)`, `Page 2 (CHUNK-002)`.
  - Expand **"Supporting Verifiable Passages"** to reveal the exact chunk.
- **Screen Action 4:** Click the sample unsupported query button: **`"❓ Unsupported: What was the CEO's favorite childhood book?"`**.
- **Screen Action 5:** Click **"🔎 Submit Grounded Query"**.
- **Expected Visual Output:** System cleanly refuses:
  ```text
  The document does not contain sufficient verifiable evidence to answer this question.
  ```
- **Spoken Voiceover:**
  > "Now we query the document. When we ask for the settlement amount, TrustLens retrieves the relevant chunks, isolates untrusted text inside strict guardrails, and provides an exact answer with verifiable physical page citations: Page 1 and Page 2.
  >
  > But if a user asks an unevidenced question—like the CEO's favorite childhood book—TrustLens strictly refuses to answer. Zero hallucinations, zero made-up citations."

---

### Segment 5: Live IBM LinuxONE Mainframe Verification (2:25 – 2:45)

- **Screen Action 1:** Alt-Tab to **Terminal 2** connected directly to `linux1@148.100.77.3`.
- **Screen Action 2:** Execute:
  ```bash
  uname -m; /home/linux1/TrustLens/.venv/bin/pytest /home/linux1/TrustLens/tests/ -q
  ```
- **Terminal Output:**
  ```text
  s390x
  ................................                                  [100%]
  32 passed in 0.27s
  ```
- **Screen Action 3:** Execute:
  ```bash
  .venv/bin/python3 scripts/validate_user_journey.py
  ```
- **Terminal Output:**
  ```text
  SUMMARY OF 11-STEP USER JOURNEY VALIDATION
  RESULT: ALL 11 STEPS FULLY PASSED AND VERIFIED!
  ```
- **Spoken Voiceover:**
  > "Everything you've seen is running right now natively on an IBM LinuxONE Community Cloud virtual server powered by the s390x IBM zArchitecture. All 32 automated security tests execute directly on the mainframe CPU in just 0.27 seconds, with zero fragile external C++ dependencies."

---

### Segment 6: Operational Audit Trail & Closing (2:45 – 3:00)

- **Screen Action 1:** Switch back to browser, click **"📜 Audit Ledger"** (or **"📊 Security Dashboard"**).
- **Visible View:** Display the tamper-evident JSON event log showing every document ingestion, SHA-256 integrity check, redaction event, and query latency timestamped in UTC.
- **Spoken Closing Voiceover:**
  > "Every single action—from hash validation to redactions and queries—is written to an immutable audit ledger with millisecond latencies for full regulatory compliance.
  >
  > TrustLens brings zero-trust security and verifiable citations to enterprise document intelligence on IBM LinuxONE. Thank you!"

---

## 3. Data Egress Disclosure: What Data Leaves the System?

| Mode | Configuration | Data Leaving Host | Destination |
| :--- | :--- | :---: | :--- |
| **Default Mode (Local Grounded)** | `ALLOW_EXTERNAL_AI=false` | **0 BYTES** | Runs 100% entirely on localhost / LinuxONE virtual machine. |
| **Optional External LLM Mode** | `ALLOW_EXTERNAL_AI=true` | **Sanitized Chunks Only** | Transmitted over TLS only to the configured endpoint (e.g. WatsonX / OpenAI). **All raw PII (credit cards, SSNs, emails, phones) is quarantined and replaced with tokens prior to transmission.** |

---

## 4. Contingency & Fallback Plans

1. **Network or External LLM Outage:**
   - TrustLens is architected to be 100% self-contained by default (`local_grounded` BM25 pipeline). It never depends on an external API to answer questions or verify evidence.
2. **SSH Port-Forwarding Disconnects:**
   - Re-run: `ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3`.
   - The Streamlit process runs as an independent daemon on the remote server; refreshing your browser instantly reconnects with session state intact.
3. **File Upload Latency:**
   - Use the built-in demo buttons (`"📄 Load Synthetic Financial Audit"` and `"📄 Load Tampered Financial Audit"`). They read directly from the server filesystem in <2 milliseconds.
4. **Terminal SSH Freeze:**
   - Run the local validation script in PowerShell: `.venv\Scripts\python.exe scripts\validate_user_journey.py` to immediately show the identical 11-step verification passing locally.
