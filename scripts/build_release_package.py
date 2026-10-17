"""
TrustLens Final Release Packager
Assembles all final release assets under submission/release/, validates hygiene,
and creates the verified release ZIP archive.
"""

import os
import shutil
import zipfile
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RELEASE_DIR = ROOT / "submission" / "release"
DIST_DIR = ROOT / "dist"
DIST_DIR.mkdir(parents=True, exist_ok=True)
ZIP_OUT_DIST = DIST_DIR / "trustlens_release.zip"
ZIP_OUT_SUBMISSION = ROOT / "submission" / "trustlens_release.zip"

FILES_TO_COPY = [
    # Core Application & Configuration
    ("app.py", "app.py"),
    ("privacy.py", "privacy.py"),
    ("integrity.py", "integrity.py"),
    ("document_qa.py", "document_qa.py"),
    ("audit.py", "audit.py"),
    ("config.py", "config.py"),
    ("requirements.txt", "requirements.txt"),
    ("Dockerfile", "Dockerfile"),
    ("docker-compose.yml", "docker-compose.yml"),
    ("pytest.ini", "pytest.ini"),
    (".env.example", ".env.example"),
    (".gitignore", ".gitignore"),
    ("README.md", "README.md"),

    # Submission deliverables
    ("submission/trustlens_pitch_deck.pdf", "trustlens_pitch_deck.pdf"),
    ("submission/pitch_deck.md", "pitch_deck.md"),
    ("submission/architecture_diagram.mmd", "architecture_diagram.mmd"),
    ("submission/architecture_diagram.html", "architecture_diagram.html"),
    ("submission/demo_script.md", "demo_script.md"),
    ("submission/final_test_report.md", "final_test_report.md"),
]

DIRS_TO_COPY = [
    ("tests", "tests", lambda f: not f.endswith(".pyc") and "__pycache__" not in f),
    ("sample_docs", "sample_docs", lambda f: True),
    ("scripts", "scripts", lambda f: not f.endswith(".pyc") and "__pycache__" not in f),
    ("docs", "docs", lambda f: True),
]

def build_release():
    print(f"Building TrustLens release under: {RELEASE_DIR}")
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copy individual files
    for src_rel, dst_rel in FILES_TO_COPY:
        src = ROOT / src_rel
        dst = RELEASE_DIR / dst_rel
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  [COPIED FILE] {src_rel} -> {dst_rel}")
        else:
            print(f"  [WARNING] File missing: {src_rel}")

    # 2. Copy directories
    for src_rel, dst_rel, filter_fn in DIRS_TO_COPY:
        src_base = ROOT / src_rel
        dst_base = RELEASE_DIR / dst_rel
        dst_base.mkdir(parents=True, exist_ok=True)

        for root, dirs, files in os.walk(src_base):
            if "__pycache__" in root:
                continue
            rel_dir = Path(root).relative_to(src_base)
            target_dir = dst_base / rel_dir
            target_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                full_src = Path(root) / file
                if filter_fn(str(full_src)):
                    full_dst = target_dir / file
                    shutil.copy2(full_src, full_dst)
        print(f"  [COPIED DIR ] {src_rel}/ -> {dst_rel}/")

    # 3. Create Release ZIP
    print("\nCreating Release ZIP Archive...")
    for zip_target in [ZIP_OUT_DIST, ZIP_OUT_SUBMISSION]:
        with zipfile.ZipFile(zip_target, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(RELEASE_DIR):
                for file in files:
                    # Skip any zip inside release dir if any
                    if file.endswith(".zip"):
                        continue
                    full_path = Path(root) / file
                    arcname = full_path.relative_to(RELEASE_DIR)
                    zf.write(full_path, arcname)

        size_kb = zip_target.stat().st_size / 1024
        # Calculate SHA256 of ZIP
        h = hashlib.sha256()
        with open(zip_target, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        sha256 = h.hexdigest()

        print(f"  [ZIP CREATED] {zip_target}")
        print(f"    Size      : {size_kb:.2f} KB ({zip_target.stat().st_size} bytes)")
        print(f"    SHA-256   : {sha256}")

    # 4. Inspect ZIP contents
    print("\nInspecting ZIP archive contents:")
    with zipfile.ZipFile(ZIP_OUT_DIST, "r") as zf:
        infolist = zf.infolist()
        total_files = len(infolist)
        print(f"  Total items in ZIP: {total_files}")
        # Test CRC
        bad_file = zf.testzip()
        if bad_file:
            print(f"  [ERROR] CRC failure on: {bad_file}")
        else:
            print("  [INTEGRITY] CRC check PASSED on all archive entries.")

if __name__ == "__main__":
    build_release()
