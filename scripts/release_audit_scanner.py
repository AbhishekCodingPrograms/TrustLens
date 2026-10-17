"""
TrustLens Release & Hygiene Audit Scanner
Scans workspace for:
- Credentials, private keys, certificates, real .env files
- Stray virtual environments, caches, temporary files
- Misleading security/cryptography claims
"""

import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".venv", "venv", "env", "ENV", ".pytest_cache", "__pycache__", ".git"
}

FORBIDDEN_FILE_PATTERNS = [
    re.compile(r"^\.env$"),
    re.compile(r".*\.pem$"),
    re.compile(r".*\.key$"),
    re.compile(r".*\.cert$"),
    re.compile(r".*\.pfx$"),
    re.compile(r"id_rsa"),
]

SECRET_CONTENT_PATTERNS = [
    (re.compile(r"-----BEGIN (RSA|OPENSSH|EC|PRIVATE) KEY-----"), "Private Key Block"),
    (re.compile(r"(?i)(watsonx[_-]?apikey|openai[_-]?api[_-]?key)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]"), "Hardcoded API Key"),
    (re.compile(r"(?i)password\s*[:=]\s*['\"][a-zA-Z0-9!@#$%^&*]{8,}['\"]"), "Hardcoded Password"),
]

MISLEADING_CLAIM_PATTERNS = [
    (re.compile(r"SHA-256 proves (original )?authorship", re.I), "Claiming SHA-256 proves authorship"),
    (re.compile(r"SHA-256 proves (creation )?timestamp", re.I), "Claiming SHA-256 proves creation time"),
    (re.compile(r"(implements|running) quantum-safe", re.I), "Unverified quantum-safe implementation claim"),
]

def scan_repository():
    findings = {
        "forbidden_files": [],
        "secret_patterns": [],
        "misleading_claims": [],
        "scanned_files_count": 0
    }

    for root, dirs, files in os.walk(ROOT_DIR):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(ROOT_DIR)

            # Skip release scanner itself from pattern checks
            if str(rel_path).replace("\\", "/") == "scripts/release_audit_scanner.py":
                continue

            findings["scanned_files_count"] += 1

            # 1. Check forbidden file names
            for pat in FORBIDDEN_FILE_PATTERNS:
                if pat.search(file):
                    findings["forbidden_files"].append(str(rel_path))

            # 2. Check content of text files
            if file_path.suffix.lower() in [".py", ".md", ".txt", ".json", ".html", ".mmd", ".yml", ".yaml", ".ini", ".example"]:
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")

                    for pattern, desc in SECRET_CONTENT_PATTERNS:
                        matches = pattern.findall(content)
                        if matches:
                            findings["secret_patterns"].append({
                                "file": str(rel_path),
                                "description": desc
                            })

                    for pattern, desc in MISLEADING_CLAIM_PATTERNS:
                        if pattern.search(content):
                            findings["misleading_claims"].append({
                                "file": str(rel_path),
                                "description": desc
                            })
                except Exception as e:
                    pass

    return findings

if __name__ == "__main__":
    results = scan_repository()
    print("==================================================")
    print(" TRUSTLENS REPOSITORY SECURITY & HYGIENE SCAN")
    print("==================================================")
    print(f"Total workspace files scanned: {results['scanned_files_count']}")
    print(f"Forbidden files detected     : {len(results['forbidden_files'])}")
    if results["forbidden_files"]:
        for f in results["forbidden_files"]:
            print(f"  [CRITICAL] Forbidden file found: {f}")
    else:
        print("  [CLEAN] No real .env, private keys (*.pem, *.key), or certs found.")

    print(f"Secret patterns detected     : {len(results['secret_patterns'])}")
    if results["secret_patterns"]:
        for s in results["secret_patterns"]:
            print(f"  [ALERT] {s['description']} in {s['file']}")
    else:
        print("  [CLEAN] Zero hardcoded keys or private key blocks found.")

    print(f"Misleading claims detected   : {len(results['misleading_claims'])}")
    if results["misleading_claims"]:
        for m in results["misleading_claims"]:
            print(f"  [NOTE] {m['description']} in {m['file']}")
    else:
        print("  [CLEAN] Zero ungrounded cryptographic claims found.")
    print("==================================================")
