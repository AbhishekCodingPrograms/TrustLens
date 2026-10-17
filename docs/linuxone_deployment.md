# TrustLens: IBM LinuxONE (`s390x`) Deployment Guide

**Competition:** IBM Z Datathon 2026  
**Theme:** AI Secured: Innovation Without Exposure  
**Target Host:** IBM LinuxONE Community Cloud Virtual Server  
**Target Architecture:** IBM zSystems / LinuxONE (`s390x`) Big-Endian 64-bit  
**Operating System:** Ubuntu 24.04.5 LTS (GNU/Linux 6.8.0-38-generic `s390x`)  

---

## 1. Architectural Philosophy & Zero-Trust Posture

TrustLens was engineered from first principles to address enterprise compliance in mainframe multi-cloud environments:

1. **Zero Fragile C++ Dependencies:** Traditional GenAI stacks rely on vector databases (ChromaDB, FAISS, hnswlib) that require complex C++ toolchains and often fail to compile or exhibit byte-ordering bugs on Big-Endian `s390x`. TrustLens implements pure-Python text extraction (`pypdf` with PyMuPDF fallback), pure-Python PDF generation (`fpdf2`), and NumPy-powered BM25 vector retrieval.
2. **Strict In-Memory Separation:** The original confidential document text is completely segregated. Automated security tests (`tests/test_document_qa.py`) verify that blocked sensitive values never enter the vector index or model prompts.
3. **Localhost-Only Network Binding:** By default, Streamlit binds exclusively to `127.0.0.1:8501`. The web interface is never exposed directly to the public internet; enterprise operators access the application via encrypted SSH local port tunneling (`-L 8501:127.0.0.1:8501`).
4. **Secret Hygiene:** Deployment archives strictly exclude `.env`, `.pem`, `.key`, and local virtual environments.

---

## 2. Server Specifications & Prerequisites

### Remote LinuxONE Environment
- **Public IP:** `148.100.77.3`
- **SSH User:** `linux1`
- **CPU:** 3 vCPUs (`s390x`)
- **RAM:** 8 GB
- **Disk:** 50 GB
- **Default SSH Key:** `$HOME\Downloads\trustlenskey.pem`

### Local Development Environment
- Windows 10/11 with PowerShell 5.1+
- OpenSSH Client (`ssh.exe`, `scp.exe` available natively in Windows System32)
- Python 3.10+ (for local testing)

---

## 3. Automated Packaging & Deployment (Recommended)

TrustLens provides automated, audited PowerShell scripts in `scripts/`:

### Step 1: Package Source Files
From the project root in Windows PowerShell, execute:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package_for_linuxone.ps1
```
*What this does:*
- Verifies that all required application and test files exist.
- Stages a clean deployment tree, strictly excluding `.env`, `*.pem`, `*.key`, `__pycache__`, and `.venv`.
- Runs automated security scans on the staging directory before packaging.
- Generates `dist\trustlens_s390x_deploy.tar.gz` and prints its SHA-256 digest.

### Step 2: Upload and Bootstrap on LinuxONE
Deploy the archive and bootstrap the virtual environment on the remote server:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\deploy_linuxone.ps1 -BootstrapRemote
```
*What this does:*
- Tests the SSH connection and confirms the remote architecture is `s390x`.
- Transfers the archive via SCP into `~/TrustLens`.
- Extracts the files remotely and cleans up the temporary archive.
- Creates a Python 3.12 virtual environment (`python3 -m venv .venv`).
- Upgrades `pip` and installs portable dependencies from `requirements.txt`.
- Executes the full 27-test automated test suite on LinuxONE natively via `pytest tests/ -v`.

---

## 4. Manual Step-by-Step Deployment (Alternative)

If you prefer to run the commands manually or deploy from a Linux terminal:

### 4.1 Transfer the Package
```powershell
# From your Windows terminal
scp -i "$HOME\Downloads\trustlenskey.pem" dist\trustlens_s390x_deploy.tar.gz linux1@148.100.77.3:~/
```

### 4.2 Connect to LinuxONE via SSH
```powershell
ssh -i "$HOME\Downloads\trustlenskey.pem" linux1@148.100.77.3
```

### 4.3 Extract and Bootstrap
```bash
# On the LinuxONE remote shell:
uname -m          # Confirms: s390x
python3 --version # Python 3.12.3

mkdir -p ~/TrustLens
mv ~/trustlens_s390x_deploy.tar.gz ~/TrustLens/
cd ~/TrustLens
tar -xzf trustlens_s390x_deploy.tar.gz
rm -f trustlens_s390x_deploy.tar.gz

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.4 Run Automated Tests on LinuxONE
```bash
pytest tests/ -v
```
All unit, privacy, integrity, RBAC, and model isolation tests must pass.

---

## 5. Launching the Application & Secure Tunneling

### 5.1 Launch Streamlit on LinuxONE (Localhost-Only)
In your SSH session on LinuxONE:
```bash
cd ~/TrustLens
source .venv/bin/activate
streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true
```
*Notice:* The server binds strictly to `127.0.0.1`, ensuring zero exposure to public IP port scanning.

### 5.2 Establish Encrypted SSH Port-Forwarding
From your local Windows machine in a separate PowerShell terminal:
```powershell
ssh -i "$HOME\Downloads\trustlenskey.pem" -L 8501:127.0.0.1:8501 linux1@148.100.77.3
```

### 5.3 Access TrustLens
Open your local browser to:
```
http://localhost:8501
```

---

## 6. Verification Checklist

| Check | Expected Result | Verified Status |
|---|---|---|
| Remote Architecture | `s390x` | ✅ Verified on Ubuntu 24.04.5 LTS |
| Dependency Portability | Zero C++ wheel compile failures | ✅ Pure-Python + NumPy stack |
| Privacy Gate Isolation | Zero sensitive PII in model prompts | ✅ Verified via automated tests |
| Evidence Grounding | Citations with page numbers, refusal on missing evidence | ✅ Verified |
| Cryptographic Integrity | SHA-256 byte-level mismatch detection | ✅ Verified |
| Tamper-Evident Audit | Chronological JSON ledger with real metrics | ✅ Verified |
| Network Security | `127.0.0.1` binding + SSH port forwarding | ✅ Hardened |
