# TrustLens: Final Submission Handoff Checklist (SUBMIT NOW)

**Competition:** IBM Z Datathon 2026  
**Track:** AI Secured: Innovation Without Exposure  
**Platform:** IBM LinuxONE Community Cloud (Ubuntu 24.04.5 LTS, `s390x`, IP: `148.100.77.3`)  
**Overall Readiness:** READY AFTER MANUAL ACTIONS (Code, artifacts, and mainframe verified)  

---

## 1. Action Items in Order of Urgency

### 🚨 Action 1 (Most Urgent): Push Repository to Public GitHub
- **Status:** **PENDING USER ACTION** (Local repository is verified and clean of secrets).
- **Exact Action Required:** Open PowerShell in `D:\IBM_IDEATHON` and run:
  ```powershell
  git init
  git add .
  git commit -m "feat(release): TrustLens final verified submission for IBM Z Datathon 2026"
  git branch -M main
  git remote add origin https://github.com/<your-username>/TrustLens.git
  git push -u origin main
  ```
- **How to Verify Successful Entry:**
  Open `https://github.com/<your-username>/TrustLens` in an incognito window. Ensure the repo is public, README displays the 32/32 tests badge, and zero `.env` or `*.pem` files are visible.
- **Portal Field Destination:** Paste the URL into **Field 6** in the submission form.

---

### 🚨 Action 2 (Most Urgent): Record 3-Minute Demonstration Video
- **Status:** **PENDING USER ACTION** (Script and live mainframe app are ready).
- **Exact Action Required:**
  1. Open a terminal and connect via SSH port forwarding:
     ```powershell
     ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3
     ```
  2. Open browser to `http://localhost:8501` (app is running live on LinuxONE).
  3. Record your screen and voiceover following [demo_rehearsal.md](file:///d:/IBM_IDEATHON/submission/FINAL_SUBMISSION/demo_rehearsal.md):
     - `0:00 - 0:30`: Problem overview on **Security Dashboard**.
     - `0:30 - 1:05`: **Integrity Gate** (`MATCH` on original, `MODIFIED` alert on tampered audit).
     - `1:05 - 1:45`: **Privacy Gate** (review 7 detected PII items, click Approve Redactions & Lock).
     - `1:45 - 2:25`: **Grounded Q&A** (query settlement amount for `Page 1 & 2` citations; query childhood book for clean refusal).
     - `2:25 - 2:45`: Alt-Tab to terminal, run `uname -m; .venv/bin/pytest tests/ -q` to prove native `s390x` execution in 0.27s.
     - `2:45 - 3:00`: Show **Audit Ledger** and wrap up.
  4. Upload video to YouTube (as Unlisted or Public), Vimeo, or Google Drive (link sharing on).
- **How to Verify Successful Entry:**
  Open the video link in an incognito window without being logged in to verify it plays publicly and duration is <= 3:00.
- **Portal Field Destination:** Paste the URL into **Field 7** in the submission form.

---

### 📄 Action 3: Upload Pitch Deck Presentation (PDF)
- **Status:** **100% READY (NO EDITING REQUIRED)**
- **Exact File Path:** `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\trustlens_pitch_deck.pdf`
- **File Metrics:** Exactly **15.25 KB** (15,611 bytes), 9 slides, PDF 1.4 landscape format.
- **How to Verify Successful Upload:**
  Check that the file size is well under the 5 MB portal limit (it is 15.25 KB).
- **Portal Field Destination:** Attach / upload as the Presentation Slide Deck.

---

### 📋 Action 4: Paste Verified Form Text Answers
- **Status:** **100% READY (COPY & PASTE READY)**
- **Source File:** [submission/FINAL_SUBMISSION/COPY_PASTE_ANSWERS.md](file:///d:/IBM_IDEATHON/submission/FINAL_SUBMISSION/COPY_PASTE_ANSWERS.md)
- **Exact Action Required:** Copy the text block from each field into the corresponding competition form input:
  - **Field 1:** Selected Challenge & Track (192 chars)
  - **Field 2:** Problem Statement (713 chars)
  - **Field 3:** Solution Overview, Architecture & Implementation (1015 chars)
  - **Field 4:** IBM Z / LinuxONE Technology Usage (958 chars)
  - **Field 5:** Value & Intended Beneficiaries (813 chars)
  - **Field 8:** Pitch Deck Location (147 chars)
  - **Field 9:** Open-Source Resources Used (498 chars)
  - **Field 10:** Supporting Documentation Links (351 chars)
- **How to Verify Successful Entry:**
  All fields are strictly <= 1024 characters, guaranteed not to be truncated.

---

### 📦 Action 5: Source Code Archive (Optional Direct Upload)
- **Status:** **100% READY (NO EDITING REQUIRED)**
- **Exact File Path:** `D:\IBM_IDEATHON\submission\FINAL_SUBMISSION\trustlens_release.zip`
- **File Metrics:** **170.27 KB** (174,361 bytes), 55 files, 100% CRC integrity verified.
- **Hygiene Verification:** Contains zero `.env`, zero `.pem` keys, zero virtual environments, and zero cache files.
- **Portal Field Destination:** Upload as supplementary zip archive if requested by portal.

---

## 2. Pre-Submission Quick Reference Table

| Required Item | Current Status | Action Needed | File Location / Reference |
| :--- | :---: | :--- | :--- |
| **GitHub Repo URL** | ⚠️ Action Required | Push code to GitHub | `https://github.com/<your-username>/TrustLens` |
| **3-Minute Video URL** | ⚠️ Action Required | Record & upload video | YouTube / Vimeo / Drive unlisted link |
| **Pitch Deck PDF** | ✅ Ready to Upload | Upload directly | `submission/FINAL_SUBMISSION/trustlens_pitch_deck.pdf` |
| **Form Text Fields** | ✅ Ready to Paste | Copy & paste fields | `submission/FINAL_SUBMISSION/COPY_PASTE_ANSWERS.md` |
| **Source Release ZIP** | ✅ Ready to Upload | Upload if required | `submission/FINAL_SUBMISSION/trustlens_release.zip` |
| **Architecture Diagram** | ✅ Verified | Available as ref | `submission/FINAL_SUBMISSION/architecture_diagram.html` |
