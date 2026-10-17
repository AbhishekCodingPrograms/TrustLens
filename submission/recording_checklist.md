# TrustLens: Final 3-Minute Video Recording Checklist & Operator Guide

**Competition:** IBM Z Datathon 2026  
**Track:** AI Secured: Innovation Without Exposure  
**Platform:** IBM LinuxONE Community Cloud (Ubuntu 24.04.5 LTS, `s390x`, IP: `148.100.77.3`)  
**Access Model:** Local Browser via SSH Port-Forwarding (`http://localhost:8501`)  
**Target Video Duration:** Exactly 3 Minutes (180 Seconds)  
**Video Resolution Target:** 1080p (1920x1080) at 30/60 fps  

---

## 1. Recording Setup & Pre-Flight Checks

### Audio & Screen Setup
- [ ] **Microphone:** Test audio levels (clear, crisp voiceover with zero echo).
- [ ] **Screen Resolution:** Set desktop resolution to 1080p (1920x1080).
- [ ] **Browser Window:** Maximize Google Chrome or Edge to `http://localhost:8501` at 100% or 110% zoom.
- [ ] **Terminal Window:** Open Windows PowerShell terminal side-by-side or behind the browser for quick `Alt-Tab` transition.

### Remote Connection Check
- [ ] **Terminal 1 (SSH Tunnel Active):**
  ```powershell
  ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3
  ```
- [ ] **Terminal 2 (Mainframe Command Ready):**
  ```powershell
  ssh -i "$HOME\Downloads\trustlenskey.pem" linux1@148.100.77.3
  ```
  *Pre-staged command in history:*
  ```bash
  uname -m; /home/linux1/TrustLens/.venv/bin/pytest /home/linux1/TrustLens/tests/ -q
  ```

---

## 2. Step-by-Step Recording Sequence (180 Seconds)

```
0:00 ─── 0:30  [Screen 1] Intro & Security Dashboard
0:30 ─── 1:05  [Screen 2] Cryptographic Document Integrity Gate
1:05 ─── 1:45  [Screen 3] Privacy Gate & Selective Masking
1:45 ─── 2:25  [Screen 4] Evidence-Grounded Q&A & Refusal
2:25 ─── 2:45  [Screen 5] Live LinuxONE Mainframe Verification
2:45 ─── 3:00  [Screen 6] Audit Ledger & Closing Statement
```

---

### Step 1: Introduction & Operational Dashboard (0:00 – 0:30)
- **Visible Screen:** Browser on `http://localhost:8501` displaying **"📊 Security Dashboard"**.
- **Action:**
  1. Hover briefly over the metric cards (*Documents Processed: 2*, *Redactions Enforced: 7*, *Integrity Checks: 2*).
  2. Point out the active role dropdown: **`Security Officer`** in the top left sidebar.
- **Spoken Audio:**
  > "Hello judges! In highly regulated domains like banking and healthcare, adopting Generative AI on confidential documents creates three major threats: leaking sensitive PII to model context windows, accepting fabricated hallucinations, and failing to detect unauthorized document alterations.
  >
  > Welcome to **TrustLens: Privacy-Gated AI with Verifiable Evidence**, running live on IBM LinuxONE. TrustLens is a zero-trust document intelligence platform that cryptographically validates document integrity, quarantines sensitive data before it reaches AI models, and provides 100% evidence-grounded answers with physical page citations."

---

### Step 2: Cryptographic Document Integrity Gate (0:30 – 1:05)
- **Visible Screen:** Click **"🔐 Integrity Gate"** in the sidebar.
- **Action 1 (Baseline Registration & Verification):**
  1. Click **`"📄 Load Synthetic Financial Audit"`** (loads `sample_docs/synthetic_financial_audit_2026.pdf`).
  2. Point cursor to the registered SHA-256 fingerprint:  
     `1c676404f87e98a9f13ce75b10a97d3dfcb9cf5b56c5bf24bbcd8546c65ffe84`
  3. In the right column, click **`"🔍 Verify Integrity Against Baseline"`**.
  4. Green banner appears:  
     `✅ INTEGRITY CHECK PASSED (MATCH): File matches registered reference 'DOC-AUDIT-2026'. Zero modifications detected.`
- **Action 2 (Tamper Detection):**
  1. Click **`"📄 Load Tampered Financial Audit"`** (loads modified document with altered \$999M escrow figure).
  2. Click **`"🔍 Verify Integrity Against Baseline"`**.
  3. Prominent red alert appears:  
     `🚨 SECURITY ALERT (MODIFIED): The file hash differs from the registered reference. The document has been modified or corrupted.`
- **Spoken Audio:**
  > "First, the Integrity Gate calculates a SHA-256 digest over the raw bytes before parsing. When we verify our authentic audit document, it matches our reference ledger exactly. But when an unauthorized party alters an escrow disbursement from \$142 Million to \$999 Million, TrustLens immediately catches the byte-level discrepancy and triggers a security alert before any model ingestion occurs."

---

### Step 3: Privacy Gate & Selective Masking (1:05 – 1:45)
- **Visible Screen:** Click **"👁️ Privacy Gate & Redaction"** in the sidebar.
- **Action:**
  1. Click **`"📄 Load Synthetic Financial Audit"`**.
  2. Review the findings table showing 7 detected entities across 4 categories:
     - Emails: `marcus.vance@continental-reserve.com`
     - Credit Card: `4***-****-****-4444`
     - Phone: `+1 (555) 349-8821`
     - Gateway IP: `10.240.12.88`
  3. Click **`"🔒 Approve Redactions & Lock for AI Processing"`**.
  4. Green confirmation appears: `Applied 7 redactions! Document locked and 2 chunks indexed for Q&A.`
  5. Click sub-tab **"🔒 Approved Redacted Text"** showing tokens `[REDACTED_EMAIL_1]`, `[REDACTED_CREDIT_CARD_6]`.
  6. Click sub-tab **"📄 Original Raw Text"** and highlight the red alert: *"Restricted View: This raw text is strictly BLOCKED from reaching the AI model."*
- **Spoken Audio:**
  > "Next is the Privacy Gate. TrustLens automatically scans extracted text across emails, phone numbers, corporate tax IDs, credit cards, and internal IPs, rendering safe masked previews. Once the compliance auditor reviews and approves redactions, the document is locked. Crucially, raw confidential text is completely quarantined in-memory—only the sanitized representation is indexed into our vector search engine."

---

### Step 4: Evidence-Grounded Q&A & Hallucination Refusal (1:45 – 2:25)
- **Visible Screen:** Click **"💡 Evidence-Grounded Q&A"** in the sidebar.
- **Action 1 (Evidenced Query):**
  1. Point to banner: *"🔒 Protected AI Pipeline Active"*.
  2. Click sample button: **`"❓ What is the settlement or reserve amount?"`**.
  3. Click **`"🔎 Submit Grounded Query"`**.
  4. Response appears citing `$142,500,000 USD` and `$14.85 Billion USD` with citations: `Page 1 (CHUNK-001)` and `Page 2 (CHUNK-002)`.
  5. Expand **"Supporting Verbatim Excerpts"** to reveal the exact chunk.
- **Action 2 (Non-Evidenced Query):**
  1. Click sample button: **`"❓ Unsupported: What was the CEO's favorite childhood book?"`**.
  2. Click **`"🔎 Submit Grounded Query"`**.
  3. System cleanly refuses:  
     `The document does not contain sufficient verifiable evidence to answer this question.`
- **Spoken Audio:**
  > "Now we query the document. When we ask for the settlement amount, TrustLens retrieves the relevant chunks, isolates untrusted text inside strict guardrails, and provides an exact answer with verifiable physical page citations: Page 1 and Page 2.
  >
  > But if a user asks an unevidenced question—like the CEO's favorite childhood book—TrustLens strictly refuses to answer. Zero hallucinations, zero made-up citations."

---

### Step 5: Live IBM LinuxONE Mainframe Proof (2:25 – 2:45)
- **Visible Screen:** Alt-Tab to **Terminal 2** connected to `linux1@148.100.77.3`.
- **Action:**
  1. Run command:
     ```bash
     uname -m; /home/linux1/TrustLens/.venv/bin/pytest /home/linux1/TrustLens/tests/ -q
     ```
  2. Terminal outputs:
     ```text
     s390x
     ................................                                  [100%]
     32 passed in 0.27s
     ```
  3. Run command:
     ```bash
     .venv/bin/python3 scripts/validate_user_journey.py
     ```
  4. Terminal outputs:
     ```text
     SUMMARY OF 11-STEP USER JOURNEY VALIDATION
     RESULT: ALL 11 STEPS FULLY PASSED AND VERIFIED!
     ```
- **Spoken Audio:**
  > "Everything you've seen is running right now natively on an IBM LinuxONE Community Cloud virtual server powered by the s390x IBM zArchitecture. All 32 automated security tests execute directly on the mainframe CPU in just 0.27 seconds, with zero fragile external C++ dependencies."

---

### Step 6: Operational Audit Ledger & Closing (2:45 – 3:00)
- **Visible Screen:** Switch back to browser, click **"📜 Audit Ledger"**.
- **Action:**
  1. Scroll through the chronological audit log showing timestamps, actor roles, SHA-256 checks, redactions, and query latencies (avg ~10 ms).
  2. Conclude cleanly.
- **Spoken Audio:**
  > "Every single action—from hash validation to redactions and queries—is recorded in an immutable audit ledger with millisecond latencies for full regulatory compliance.
  >
  > TrustLens brings zero-trust security and verifiable citations to enterprise document intelligence on IBM LinuxONE. Thank you!"

---

## 3. Post-Recording Quality Verification Checklist

- [ ] Video duration is strictly between **2:45 and 3:00** (under the 3:00 limit).
- [ ] No private keys or `.env` files shown on screen.
- [ ] Audio is synchronized with screen actions.
- [ ] Uploaded as **Unlisted** or **Public** on YouTube (or Vimeo / Drive with public link sharing enabled).
- [ ] Inserted the video URL into **Field 7** in `submission/final_form_answers.md`.
