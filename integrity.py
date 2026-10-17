"""
TrustLens Document Integrity Module
Provides SHA-256 cryptographic hashing, reference registration,
tamper detection, and audit trail verification.
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from config import INTEGRITY_LEDGER_PATH


class IntegrityManager:
    """Manages document hash calculation, registration, and modification detection."""

    def __init__(self, ledger_path: Path = INTEGRITY_LEDGER_PATH):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_ledger_exists()

    def _ensure_ledger_exists(self) -> None:
        """Initializes empty ledger structure if not present."""
        if not self.ledger_path.exists():
            initial_data = {
                "version": "1.0",
                "disclaimer": "SHA-256 hashes detect byte-level changes relative to a trusted reference record; they prove consistency, not legal authorship.",
                "registered_documents": {},
                "verification_history": []
            }
            self._save_ledger(initial_data)

    def _load_ledger(self) -> dict:
        """Loads the current ledger from disk."""
        try:
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"registered_documents": {}, "verification_history": []}

    def _save_ledger(self, data: dict) -> None:
        """Saves ledger data to disk atomically."""
        tmp_path = self.ledger_path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, self.ledger_path)

    @staticmethod
    def calculate_sha256(data: bytes) -> str:
        """Calculates standard SHA-256 hash for byte content."""
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Data for SHA-256 calculation must be bytes or bytearray.")
        hasher = hashlib.sha256()
        hasher.update(data)
        return hasher.hexdigest().lower()

    @staticmethod
    def calculate_text_sha256(text: str) -> str:
        """Calculates SHA-256 hash for UTF-8 encoded text."""
        return IntegrityManager.calculate_sha256(text.encode("utf-8"))

    def register_reference(
        self,
        document_id: str,
        filename: str,
        file_bytes: bytes,
        notes: str = ""
    ) -> dict:
        """Registers a document's SHA-256 hash as the baseline reference."""
        sha256_hash = self.calculate_sha256(file_bytes)
        now_utc = datetime.now(timezone.utc).isoformat()
        file_size = len(file_bytes)

        ledger = self._load_ledger()
        if "registered_documents" not in ledger:
            ledger["registered_documents"] = {}

        record = {
            "document_id": document_id,
            "filename": filename,
            "sha256_hash": sha256_hash,
            "registered_at": now_utc,
            "file_size_bytes": file_size,
            "notes": notes,
            "verification_count": 0
        }

        ledger["registered_documents"][document_id] = record
        self._save_ledger(ledger)

        return record

    def verify_file(
        self,
        file_bytes: bytes,
        reference_id: Optional[str] = None,
        expected_hash: Optional[str] = None,
        filename: str = "uploaded_file"
    ) -> dict:
        """
        Verifies uploaded file bytes against a registered document ID or an expected SHA-256 hash.
        Detects byte-level modifications and records verification outcome.
        """
        current_hash = self.calculate_sha256(file_bytes)
        now_utc = datetime.now(timezone.utc).isoformat()
        ledger = self._load_ledger()

        target_ref = None
        if reference_id and reference_id in ledger.get("registered_documents", {}):
            target_ref = ledger["registered_documents"][reference_id]
            expected_hash = target_ref["sha256_hash"]
        elif expected_hash:
            expected_hash = expected_hash.strip().lower()
            # Search if any registered doc matches this hash
            for doc_id, doc in ledger.get("registered_documents", {}).items():
                if doc.get("sha256_hash") == expected_hash:
                    target_ref = doc
                    reference_id = doc_id
                    break

        if not expected_hash:
            # Check if this hash is already known in ledger
            matched_doc_id = None
            for doc_id, doc in ledger.get("registered_documents", {}).items():
                if doc.get("sha256_hash") == current_hash:
                    matched_doc_id = doc_id
                    target_ref = doc
                    break

            if matched_doc_id:
                status = "MATCH"
                message = f"File matches registered reference '{matched_doc_id}' ({target_ref.get('filename')}). Document is unmodified."
                reference_id = matched_doc_id
                expected_hash = current_hash
            else:
                status = "NOT_REGISTERED"
                message = "File is not yet registered in the integrity ledger. Calculate hash and register to establish a baseline."
        else:
            if current_hash == expected_hash:
                status = "MATCH"
                message = "Integrity check PASSED. File bytes match the registered reference exactly. Zero modifications detected."
            else:
                status = "MODIFIED"
                message = "SECURITY WARNING: Integrity check FAILED. The file hash differs from the registered reference. The document has been modified or corrupted."

        result = {
            "status": status,  # "MATCH", "MODIFIED", or "NOT_REGISTERED"
            "current_hash": current_hash,
            "expected_hash": expected_hash,
            "reference_id": reference_id,
            "filename": filename,
            "file_size_bytes": len(file_bytes),
            "verified_at": now_utc,
            "message": message,
            "disclaimer": "Cryptographic hashes verify byte-level integrity relative to the reference; they do not attest to original authorship."
        }

        # Update verification history in ledger
        if "verification_history" not in ledger:
            ledger["verification_history"] = []
        ledger["verification_history"].append(result)

        if status == "MATCH" and reference_id and reference_id in ledger.get("registered_documents", {}):
            ledger["registered_documents"][reference_id]["verification_count"] = (
                ledger["registered_documents"][reference_id].get("verification_count", 0) + 1
            )

        self._save_ledger(ledger)
        return result

    def get_registered_documents(self) -> Dict[str, dict]:
        """Returns all registered reference documents."""
        ledger = self._load_ledger()
        return ledger.get("registered_documents", {})

    def get_verification_history(self) -> List[dict]:
        """Returns the chronological verification logs."""
        ledger = self._load_ledger()
        return ledger.get("verification_history", [])
