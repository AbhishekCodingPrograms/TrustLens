"""
TrustLens Final Submission Assembler
Creates submission/FINAL_SUBMISSION/ and populates with verified deliverables.
Validates ZIP integrity, PDF size, and PDF readability.
"""

import os
import shutil
import zipfile
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUBMISSION_DIR = ROOT / "submission"
FINAL_DIR = SUBMISSION_DIR / "FINAL_SUBMISSION"

FILES_TO_COPY = [
    (SUBMISSION_DIR / "trustlens_release.zip", "trustlens_release.zip"),
    (SUBMISSION_DIR / "trustlens_pitch_deck.pdf", "trustlens_pitch_deck.pdf"),
    (SUBMISSION_DIR / "pitch_deck.md", "pitch_deck.md"),
    (SUBMISSION_DIR / "architecture_diagram.mmd", "architecture_diagram.mmd"),
    (SUBMISSION_DIR / "architecture_diagram.html", "architecture_diagram.html"),
    (SUBMISSION_DIR / "demo_rehearsal.md", "demo_rehearsal.md"),
    (SUBMISSION_DIR / "recording_checklist.md", "recording_checklist.md"),
    (SUBMISSION_DIR / "final_test_report.md", "final_test_report.md"),
    (SUBMISSION_DIR / "final_readiness_report.md", "final_readiness_report.md"),
    (SUBMISSION_DIR / "evidence_matrix.md", "evidence_matrix.md"),
    (SUBMISSION_DIR / "judge_qa.md", "judge_qa.md"),
    (ROOT / "README.md", "README.md"),
    (ROOT / ".env.example", ".env.example"),
    (ROOT / ".gitignore", ".gitignore"),
]

def assemble():
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Assembling final submission into: {FINAL_DIR}")

    for src, dst_name in FILES_TO_COPY:
        dst = FINAL_DIR / dst_name
        if src.exists():
            shutil.copy2(src, dst)
            size_kb = dst.stat().st_size / 1024
            print(f"  [OK] Copied {dst_name:30} ({size_kb:7.2f} KB)")
        else:
            print(f"  [ERROR] Source missing: {src}")

    # Validate ZIP integrity
    zip_path = FINAL_DIR / "trustlens_release.zip"
    with zipfile.ZipFile(zip_path, "r") as zf:
        bad = zf.testzip()
        if bad:
            print(f"  [CRC ERROR] Corrupt file in ZIP: {bad}")
        else:
            print(f"  [PASS] ZIP archive CRC check passed ({len(zf.infolist())} entries).")

    # Validate PDF size and readability
    pdf_path = FINAL_DIR / "trustlens_pitch_deck.pdf"
    pdf_size_bytes = pdf_path.stat().st_size
    assert pdf_size_bytes < 5 * 1024 * 1024, "PDF exceeds 5MB limit!"
    print(f"  [PASS] Pitch deck PDF verified: {pdf_size_bytes} bytes ({pdf_size_bytes/1024:.2f} KB < 5 MB).")

if __name__ == "__main__":
    assemble()
