# TrustLens 3-Minute Hackathon Demonstration Script
**IBM Z Datathon 2026**  
**Theme:** AI Secured: Innovation Without Exposure  

---

## Demo Overview (Total Duration: 3 Minutes)

This demonstration shows how **TrustLens** ingests a confidential enterprise document, detects tampering via cryptographic SHA-256 hashing, intercepts and redacts sensitive PII before AI processing, answers user questions using verifiable evidence with page citations, and refuses to hallucinate when evidence is absent.

---

### Step 1: System Overview & Platform Status (0:00 - 0:30)
- **Visual:** Open Streamlit Dashboard (`http://localhost:8501`).
- **Narrator Script:**
  > "Welcome to TrustLens: Privacy-Gated AI with Verifiable Evidence, built for the IBM Z Datathon 2026 under the theme 'AI Secured: Innovation Without Exposure'.
  >
  > In enterprise environments like IBM LinuxONE, analyzing confidential records with generative AI creates severe vulnerabilities: sensitive data leakage to external models, hallucinated citations, and prompt injection.
  >
  > Notice on our sidebar: TrustLens displays real runtime platform metrics, detects the LinuxONE host architecture, provides a 3-tier Role-Based Access Control persona switcher (Security Officer, Compliance Auditor, Restricted Viewer), and enforces a strict zero-trust default—no confidential byte leaves this system without explicit human consent."

---

### Step 2: Cryptographic Integrity Gate & Tamper Detection (0:30 - 1:15)
- **Visual:** Navigate to **🔐 Integrity Gate**.
- **Action 1:** Upload `sample_docs/synthetic_financial_audit_2026.pdf`.
  - Click **Register as Reference Baseline**.
  - Show the computed SHA-256 digest and registered entry in the ledger.
- **Action 2:** Upload the tampered document `sample_docs/synthetic_tampered_financial_audit.pdf`.
  - Click **Verify Integrity Against Baseline**.
- **Visual Outcome:**
  - Red security banner appears: **`🚨 SECURITY ALERT (MODIFIED): The file hash differs from the registered reference.`**
- **Narrator Script:**
  > "First, we establish verifiable document integrity. We upload our annual financial audit and register its baseline SHA-256 cryptographic fingerprint in our tamper-evident ledger.
  >
  > Next, to test security, an unauthorized actor attempts to upload a modified version where an escrow disbursement was altered from \$142 Million to \$999 Million.
  >
  > TrustLens calculates the hash over raw bytes, instantly catches the mismatch, and flags the modification before any AI processing can occur."

---

### Step 3: Privacy Gate & Selective Redaction (1:15 - 2:05)
- **Visual:** Navigate to **👁️ Privacy Gate & Redaction**.
- **Action 1:** Load `synthetic_financial_audit_2026.pdf`.
- **Visual Outcome:**
  - Table displays detected sensitive items:
    - Auditor Email: `marcus.vance@continental-reserve.com`
    - Phone: `+1 (555) 349-8821`
    - Tax ID: `12-3456789`
    - Credit Card: `4111222233334444`
    - Gateway IP: `10.240.12.88`
- **Action 2:** Checkboxes show selective redaction controls. Click **🔒 Approve Redactions & Lock for AI Processing**.
- **Visual Outcome:**
  - Green confirmation banner appears.
  - Tab shows **Sanitized Document View**: PII replaced with `[REDACTED_EMAIL_1]`, `[REDACTED_PHONE_2]`, etc.
  - Download Sanitized PDF button becomes available.
- **Narrator Script:**
  > "Now we enter the Privacy Gate. TrustLens automatically scans the document across pages, detecting email addresses, direct phone numbers, corporate tax IDs, payment cards, and network IPs.
  >
  > The user has full selective control. When we click 'Approve Redactions and Lock', TrustLens creates a sanitized in-memory document.
  >
  > Crucially, our automated tests prove that the original confidential strings are completely blocked from entering the AI model prompt or vector store."

---

### Step 4: Evidence-Grounded Q&A & Refusal to Hallucinate (2:05 - 2:45)
- **Visual:** Navigate to **💡 Evidence-Grounded Q&A**.
- **Action 1:** Click sample query: *"What is the settlement or reserve amount?"*
  - Click **Submit Grounded Query**.
- **Visual Outcome:**
  - Green badge: **`✅ Verified with Verifiable Document Evidence`**.
  - Answer states \$4.85 Billion USD Tier-1 capital reserves and \$142,500,000 USD settlement disbursement.
  - Cites **`Page 1 (CHUNK-001)`** and **`Page 2 (CHUNK-002)`**.
  - Expanders reveal the verbatim supporting excerpts.
  - Latency displayed: `< 5 ms`.
- **Action 2:** Click sample query: *"What is the Mars orbital speed?"*
  - Click **Submit Grounded Query**.
- **Visual Outcome:**
  - Red notice: **`🚫 Insufficient Evidence in Approved Document`**.
  - Message: *"The document does not contain sufficient verifiable evidence to answer this question."*
  - Citations list: Empty.
- **Narrator Script:**
  > "In the Evidence-Grounded Q&A module, we ask for the settlement amount. TrustLens retrieves the relevant chunks, validates the evidence, and generates a grounded response citing Page 1 and Page 2 with exact verbatim excerpts.
  >
  > Now, what happens if a user asks a question not in the document—like the orbital speed of Mars?
  >
  > Instead of hallucinating a believable falsehood, TrustLens's strict evidence threshold immediately identifies that zero substantive evidence exists and explicitly rejects the inquiry. Zero hallucination, 100% verifiable grounding."

---

### Step 5: Security Audit Ledger & Conclusion (2:45 - 3:00)
- **Visual:** Navigate to **📊 Security Dashboard** and **📜 Audit Ledger**.
- **Visual Outcome:**
  - Dashboard shows updated real counts: Documents processed, sensitive items detected, redactions performed, integrity checks passed and failed, and actual measured latency.
  - Audit Ledger displays the chronological event trail.
- **Narrator Script:**
  > "Finally, the Security Dashboard tracks every ingestion, redaction, integrity alert, and query with real, un-fabricated operational metrics. The entire audit trail is exportable as JSON.
  >
  > TrustLens delivers genuine AI security: empowering innovation on IBM LinuxONE without exposing confidential data. Thank you!"
