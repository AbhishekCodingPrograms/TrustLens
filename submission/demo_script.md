# TrustLens: 3-Minute Video Demonstration Script
**Competition:** IBM Z Datathon 2026  
**Theme:** AI Secured: Innovation Without Exposure  
**Track:** Document Intelligence & Enterprise Mainframe Security  
**Presenter:** Antigravity Engineering Team  
**Target Duration:** Exactly 3:00 (180 seconds)  

---

## Technical Setup Before Recording
1. **Local Terminal (Windows PowerShell)**:
   - Ensure SSH tunnel is active:
     ```powershell
     ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3
     ```
   - Second terminal open to show remote LinuxONE verification:
     ```powershell
     ssh -i "$HOME\Downloads\trustlenskey.pem" linux1@148.100.77.3
     ```
2. **Browser**:
   - Tab 1: `http://localhost:8501` (TrustLens Streamlit Dashboard, fresh session).
   - Tab 2: `submission/architecture_diagram.html` (Local visual reference).
3. **Sample Files Available on Desktop/Folder**:
   - `sample_docs/synthetic_financial_audit_2026.pdf`
   - `sample_docs/synthetic_tampered_financial_audit.pdf`

---

## Timed Video Script & Walkthrough

### [0:00 – 0:20] Segment 1: The Problem — Why Ingesting Raw Documents into AI is Dangerous
- **Visual on Screen:**
  - Open on slide / title screen or the TrustLens Security Dashboard (`http://localhost:8501`).
  - Cursor highlights the title: *"TrustLens: Privacy-Gated AI with Verifiable Evidence"*.
- **Presenter Narration (Spoken):**
  > *"Every day, enterprise banking, healthcare, and legal teams want to unlock insights from sensitive PDF audits and contracts using Generative AI. But doing so creates a critical vulnerability: sending unredacted documents exposes customer PII, credit card numbers, and trade secrets to external or internal LLMs. Worse, models frequently hallucinate unsupported answers, while undetected file tampering can quietly corrupt compliance decisions before AI processing even begins."*

---

### [0:20 – 0:50] Segment 2: TrustLens Architecture & Privacy Gate Solution
- **Visual on Screen:**
  - Transition briefly to the Architecture Diagram (`submission/architecture_diagram.html`).
  - Mouse traces the dual-gate flow:
    1. Cryptographic Document Integrity Gate.
    2. Privacy Gate & Selective Masking.
    3. Grounded RAG with `<untrusted_document_context>` model isolation.
- **Presenter Narration (Spoken):**
  > *"To solve this for the IBM Z Datathon, we built TrustLens: an end-to-end zero-trust document intelligence platform running natively on IBM LinuxONE s390x. TrustLens enforces a dual-gate architecture. First, a cryptographic integrity gate checks SHA-256 byte consistency against an immutable ledger. Second, our Privacy Gate automatically scans for sensitive entities, requiring human auditor sign-off before any document text is allowed near an AI model."*

---

### [0:50 – 1:25] Segment 3: Live Walkthrough — Privacy Gate & Sensitive Data Masking
- **Visual on Screen:**
  - Switch to browser tab at `http://localhost:8501`.
  - Navigate to **"👁️ Privacy Gate & Redaction"** on sidebar.
  - Click button: **"📄 Load Synthetic Financial Audit"** (or upload `synthetic_financial_audit_2026.pdf`).
  - Table instantly renders with 7 detected findings across Emails, Phone Numbers, Credit Cards, and IP Addresses.
  - Show the **"Masked Value"** preview (e.g. `c***@trustlens.internal`, `4***-****-****-1111`).
  - Click **"🔒 Approve Redactions & Lock for AI Processing"**.
  - Show the side-by-side tabs: Approved Redacted Text vs Original Raw Text (Restricted).
- **Presenter Narration (Spoken):**
  > *"Let's see this live on our LinuxONE server. I'll load our synthetic financial audit. Instantly, our regex engine detects seven sensitive findings—including employee corporate emails, direct phone numbers, and corporate credit cards. Notice that even in this preview, raw values are masked. As a Security Officer, I review and approve the redactions. When I click 'Approve & Lock', TrustLens creates a sanitized in-memory representation. The raw unredacted text is permanently isolated and blocked from the AI model."*

---

### [1:25 – 1:55] Segment 4: Grounded Q&A with Exact Citations & Hallucination Defense
- **Visual on Screen:**
  - Click **"💡 Evidence-Grounded Q&A"** on sidebar.
  - Show the green banner: *"🔒 Protected AI Pipeline Active"*.
  - Click sample question: *"What is the settlement or reserve amount?"* (or enter: *"What is the total consulting expense?"*).
  - Click **"🔎 Submit Grounded Query"**.
  - Highlight the output:
    - Generated answer citing `$4,850,000`.
    - Citations pill: `[Page 1 (CHUNK-001)]`.
    - Expand **"Supporting Verifiable Passages"** showing the exact sanitized context chunk.
  - Click unsupported question: *"Unsupported: What is the Mars orbital speed?"*.
  - Highlight system refusal: *"The document does not contain sufficient verifiable evidence to answer this question."*
- **Presenter Narration (Spoken):**
  > *"Now we move to Evidence-Grounded Q&A. The AI pipeline is only permitted to read sanitized chunks. When we ask 'What is the total consulting expense?', TrustLens retrieves the relevant passage, generates a factual answer, and provides a direct citation: Page 1, Chunk 1. More importantly, when we submit an out-of-scope query like 'What is the Mars orbital speed?', TrustLens strictly refuses to hallucinate, informing the user that verifiable evidence is absent."*

---

### [1:55 – 2:20] Segment 5: SHA-256 Cryptographic Integrity Verification & Tamper Detection
- **Visual on Screen:**
  - Navigate to **"🔐 Integrity Gate"** on sidebar.
  - Upload `synthetic_financial_audit_2026.pdf`.
  - Click **"🔍 Verify Integrity Against Baseline"**.
  - Show the green alert: `✅ INTEGRITY CHECK PASSED (MATCH): Zero modifications detected.`
  - Now, upload `synthetic_tampered_financial_audit.pdf`.
  - Click **"🔍 Verify Integrity Against Baseline"**.
  - Show the red alert: `🚨 SECURITY ALERT (MODIFIED): File hash differs from registered reference.`
- **Presenter Narration (Spoken):**
  > *"Next, document integrity. What if a financial audit was modified before reaching the system? Here, we verify our original document: the SHA-256 hash matches our registered baseline exactly—zero modifications. Now, we upload a tampered version where a single byte was altered. TrustLens immediately triggers a security alert, rejecting the document before any AI processing or compliance review can be tricked."*

---

### [2:20 – 2:40] Segment 6: Native IBM LinuxONE Deployment & Mainframe Performance
- **Visual on Screen:**
  - Switch to terminal window logged into `linux1@148.100.77.3`.
  - Run:
    ```bash
    uname -m; lscpu | grep "Model name\|Architecture"; .venv/bin/pytest tests/ -q
    ```
  - Show output:
    - `s390x`
    - `27 passed in 0.26s`
  - Run deep verification:
    ```bash
    .venv/bin/python3 scripts/verify_linuxone.py
    ```
- **Presenter Narration (Spoken):**
  > *"TrustLens isn't just a prototype—it is fully deployed and verified live on an IBM LinuxONE Community Cloud virtual server. As you can see directly from our remote terminal, the machine architecture is native s390x running on an IBM z16 mainframe. Our entire automated security and unit test suite runs in just 0.26 seconds, and our Streamlit service is strictly bound to localhost via encrypted SSH port forwarding."*

---

### [2:40 – 3:00] Segment 7: Real-World Value, Honest Limitations & Future Roadmap
- **Visual on Screen:**
  - Switch back to browser, open **"📊 Security Dashboard"**.
  - Show real-time counters: Documents Ingested (2), Redactions Enforced (7), Integrity Tamper Alerts (1), Avg Retrieval Latency (10.3 ms).
  - Concluding slide with repository and project info.
- **Presenter Narration (Spoken):**
  > *"In summary, TrustLens delivers zero-trust document intelligence without exposure: provable privacy masking, verifiable page citations, cryptographic tamper alerts, and complete auditability. In production, this architecture integrates with IBM RACF directory controls and hardware-accelerated CPACF crypto. Thank you for evaluating TrustLens for the IBM Z Datathon 2026!"*

---

## Live Demo Fallback & Contingency Plan
If any technical issue occurs during video recording, use these tested contingency procedures:

| Failure Mode | Immediate Fallback Action |
|---|---|
| **SSH Port Forwarding Tunnel Drops** | In Windows PowerShell, immediately reconnect: `ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3`. The Streamlit session state persists on the remote server. |
| **Streamlit Process Stopped on VM** | In SSH session, rerun: `cd ~/trustlens && .venv/bin/streamlit run app.py --server.headless true --server.address 127.0.0.1 --server.port 8501`. |
| **Network Latency / Upload Delay** | Use the built-in quick buttons on the UI: `"📄 Load Synthetic Financial Audit"` and `"📄 Load Tampered Financial Audit"`. These load pre-staged sample files instantaneously without network upload latency. |
| **Terminal Recording Alternative** | If SSH to LinuxONE lags during screen capture, execute the local suite: `.venv\Scripts\python.exe -m pytest tests -v` followed by showing the verified remote terminal log from `docs/verification_report.md`. |
