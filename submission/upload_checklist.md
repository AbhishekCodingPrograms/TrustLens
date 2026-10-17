# TrustLens: Final Submission Upload Checklist

**Competition:** IBM Z Datathon 2026  
**Track:** AI Secured: Innovation Without Exposure  
**Target Platform:** IBM LinuxONE Community Cloud (Ubuntu 24.04.5 LTS, `s390x`, IP: `148.100.77.3`)  
**Audit Date:** October 18, 2026  
**Release Version:** v1.0.0-final  

---

## 1. Deliverables Verification Table

| # | Required Datathon Deliverable | Actual Local File Path / URL | Verification Status | Exact Size / Metrics | Remaining Manual Action by Submitter |
| :-: | :--- | :--- | :---: | :--- | :--- |
| **1** | **Source Code Package (ZIP)** | `D:\IBM_IDEATHON\dist\trustlens_release.zip` | **VERIFIED (PASS)** | **158.45 KB** (162,251 bytes), 51 files, 100% CRC pass | Ready to upload directly if portal requests a ZIP archive. |
| **2** | **Public GitHub Repository URL** | `[ACTION REQUIRED: Insert GitHub URL]` | **ACTION REQUIRED** | Git repository initialized, `.gitignore` excludes secrets | Push local repo to public GitHub and paste URL in Field 6. |
| **3** | **Pitch Deck Presentation (PDF)** | `D:\IBM_IDEATHON\submission\trustlens_pitch_deck.pdf` | **VERIFIED (PASS)** | **15.25 KB** (15,611 bytes), 9 slides (well below 5 MB ceiling) | Upload this PDF file directly to the hackathon portal. |
| **4** | **3-Minute Video Demo URL** | `[ACTION REQUIRED: Insert Video URL]` | **ACTION REQUIRED** | Walkthrough script timed to exactly 180 seconds | Record screen using `recording_checklist.md`, upload to YouTube/Vimeo/Drive, paste link in Field 7. |
| **5** | **Problem Statement** | [submission/final_form_answers.md](file:///d:/IBM_IDEATHON/submission/final_form_answers.md) (Field 2) | **VERIFIED (PASS)** | 713 characters (<= 1024 limit) | Copy text into submission portal field. |
| **6** | **Project Overview & Architecture** | [submission/final_form_answers.md](file:///d:/IBM_IDEATHON/submission/final_form_answers.md) (Field 3) | **VERIFIED (PASS)** | 1015 characters (<= 1024 limit) | Copy text into submission portal field. |
| **7** | **IBM Z / LinuxONE Usage Description** | [submission/final_form_answers.md](file:///d:/IBM_IDEATHON/submission/final_form_answers.md) (Field 4) | **VERIFIED (PASS)** | 958 characters (<= 1024 limit) | Copy text into submission portal field. |
| **8** | **Project Value & Beneficiaries** | [submission/final_form_answers.md](file:///d:/IBM_IDEATHON/submission/final_form_answers.md) (Field 5) | **VERIFIED (PASS)** | 813 characters (<= 1024 limit) | Copy text into submission portal field. |
| **9** | **Open-Source Resource URLs** | [submission/final_form_answers.md](file:///d:/IBM_IDEATHON/submission/final_form_answers.md) (Field 9) | **VERIFIED (PASS)** | 498 characters (<= 1024 limit) | Copy text into submission portal field. |
| **10**| **Supporting Documentation Links** | [submission/final_form_answers.md](file:///d:/IBM_IDEATHON/submission/final_form_answers.md) (Field 10) | **VERIFIED (PASS)** | 340 characters (<= 1024 limit) | Copy text into submission portal field. |

---

## 2. Pre-Upload Sanity & Hygiene Checklist

- [x] **Zero Credentials Stored:** Verified 0 private SSH keys (`trustlenskey.pem` is strictly in local `$HOME\Downloads` and excluded by `.gitignore`).
- [x] **Zero Real `.env` Files:** Verified only clean [.env.example](file:///d:/IBM_IDEATHON/.env.example) with placeholders exists in the project and release archive.
- [x] **Zero Virtual Environments in Release:** Verified `.venv/` and `__pycache__/` are 100% excluded from `trustlens_release.zip`.
- [x] **Zero Fabricated Cryptographic Claims:** All SHA-256 statements specify byte-level consistency relative to a reference baseline; zero claims of proving original human authorship or timestamps.
- [x] **Live LinuxONE Proof:** LinuxONE server (`148.100.77.3`) confirmed running Streamlit under PID `12799`, responding with `HTTP 200 OK` on `127.0.0.1:8501`.
- [x] **Portal Character Limit Compliance:** All form answer fields confirmed <= 1024 characters via `scripts/verify_form_answers.py`.

---

## 3. Human Actions Required to Complete Submission

1. **Step 1: Push Code to GitHub**
   ```powershell
   git init
   git add .
   git commit -m "feat(release): TrustLens final verified submission for IBM Z Datathon 2026"
   git branch -M main
   git remote add origin https://github.com/<your-username>/TrustLens.git
   git push -u origin main
   ```
2. **Step 2: Record 3-Minute Video**
   - Connect SSH tunnel: `ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3`
   - Open browser to `http://localhost:8501`.
   - Record following [submission/recording_checklist.md](file:///d:/IBM_IDEATHON/submission/recording_checklist.md).
   - Upload video to YouTube (unlisted or public), Vimeo, or Google Drive.
3. **Step 3: Submit on Competition Portal**
   - Open [submission/final_form_answers.md](file:///d:/IBM_IDEATHON/submission/final_form_answers.md).
   - Replace `[ACTION REQUIRED]` in Field 6 with your GitHub repository URL.
   - Replace `[ACTION REQUIRED]` in Field 7 with your video demonstration URL.
   - Copy fields into the submission portal and attach [submission/trustlens_pitch_deck.pdf](file:///d:/IBM_IDEATHON/submission/trustlens_pitch_deck.pdf).
