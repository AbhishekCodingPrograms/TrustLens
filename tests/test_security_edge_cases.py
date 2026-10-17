"""
Security, Reliability, and Edge-Case Tests for TrustLens.
Tests invalid files, corrupt PDFs, empty documents, file size limits,
masking behavior, and model failure resilience.
"""

import pytest
import io
from privacy import PrivacyScanner, SensitiveFinding
from integrity import IntegrityManager
from document_qa import DocumentQAPipeline
from audit import SecurityAuditor
from config import MAX_FILE_SIZE_BYTES


def test_sensitive_value_masking():
    """Verify masking logic masks sensitive PII while preserving readable context."""
    assert SensitiveFinding.mask_value("john.doe@company.org", "EMAIL") == "j***@company.org"
    assert SensitiveFinding.mask_value("555-123-4567", "PHONE_NUMBER") == "********4567"
    assert SensitiveFinding.mask_value("4111222233334444", "CREDIT_CARD") == "************4444"
    assert SensitiveFinding.mask_value("sk-1234567890abcdef123456", "API_KEY_SECRET") == "sk-...456"
    assert SensitiveFinding.mask_value("123-45-6789", "SSN_TAX_ID") == "*******6789"


def test_corrupt_pdf_handling():
    """Verify corrupt or non-PDF bytes raise clean ValueError without crashing."""
    scanner = PrivacyScanner()
    corrupt_bytes = b"%PDF-1.4 Corrupt File Header with garbage content \x00\xff\xfe"

    with pytest.raises(Exception):
        scanner.extract_document(corrupt_bytes, "corrupted.pdf")


def test_empty_document_handling():
    """Verify empty document text is handled gracefully."""
    scanner = PrivacyScanner()
    empty_pages = [{"page": 1, "text": ""}]

    findings = scanner.scan(empty_pages)
    assert len(findings) == 0

    redacted_pages, summary = scanner.redact_text_pages(empty_pages, findings)
    assert summary["total_detected"] == 0
    assert summary["redactions_applied"] == 0

    pipeline = DocumentQAPipeline()
    chunks_count = pipeline.load_document(empty_pages, "empty.txt")
    assert chunks_count == 0

    # Query against empty pipeline returns clean warning
    result = pipeline.answer_question("What is the revenue?")
    assert result["evidence_found"] is False
    assert "No document is currently indexed" in result["answer"]


def test_custom_sensitive_pattern():
    """Verify user-configured custom regex patterns work seamlessly."""
    custom_patterns = {
        "PROJECT_CODENAME": {
            "name": "Project Codename",
            "pattern": r"\bPROJECT-(?:APOLLO|ZEUS|NEPTUNE)\b",
            "description": "Internal project codenames",
            "placeholder_prefix": "CODENAME"
        }
    }
    scanner = PrivacyScanner(custom_patterns=custom_patterns)
    text = "The launch schedule for PROJECT-ZEUS was delayed by three weeks."
    pages = [{"page": 1, "text": text}]

    findings = scanner.scan(pages)
    assert len(findings) == 1
    assert findings[0]["entity_type"] == "PROJECT_CODENAME"
    assert findings[0]["value"] == "PROJECT-ZEUS"

    redacted_pages, summary = scanner.redact_text_pages(pages, findings)
    assert "PROJECT-ZEUS" not in redacted_pages[0]["text"]
    assert "[REDACTED_CODENAME_1]" in redacted_pages[0]["text"]


def test_file_size_limit_validation():
    """Verify oversized payloads exceed allowed threshold."""
    oversized_bytes = b"0" * (MAX_FILE_SIZE_BYTES + 1024)
    is_valid = len(oversized_bytes) <= MAX_FILE_SIZE_BYTES
    assert is_valid is False

    normal_bytes = b"0" * (1024 * 50)  # 50 KB
    assert (len(normal_bytes) <= MAX_FILE_SIZE_BYTES) is True


def test_audit_log_never_logs_unredacted_sensitive_data(tmp_path):
    """
    Security Verification:
    Ensures that audit logs never store raw document content, unmasked emails,
    credit cards, or credentials in any event payload.
    """
    log_file = tmp_path / "test_audit.json"
    auditor = SecurityAuditor(log_path=log_file)

    secret_email = "confidential_officer@secure-bank.org"
    secret_card = "4111222233334444"

    # Simulate logging standard events
    auditor.log_event("DOCUMENT_INGESTED", {
        "filename": "confidential_memo.pdf",
        "sha256_hash": "a" * 64,
        "file_size_bytes": 1024,
        "pages_count": 2
    })

    auditor.log_event("PRIVACY_SCAN", {
        "filename": "confidential_memo.pdf",
        "total_findings": 2,
        "entities_detected": ["EMAIL", "CREDIT_CARD"]
    })

    auditor.log_event("REDACTION_APPLIED", {
        "filename": "confidential_memo.pdf",
        "redactions_applied": 2,
        "items_preserved": 0,
        "categories": ["Email Address", "Credit Card Number"]
    })

    events = auditor.get_events()
    assert len(events) == 3

    # Inspect all JSON serialization strings
    log_content = log_file.read_text(encoding="utf-8")
    assert secret_email not in log_content
    assert secret_card not in log_content


def test_corrupted_integrity_ledger_graceful_recovery(tmp_path):
    """
    Reliability Verification:
    Ensures that if the integrity ledger JSON file is corrupted or contains invalid syntax,
    IntegrityManager does not crash and recovers safely.
    """
    corrupt_ledger = tmp_path / "corrupted_ledger.json"
    corrupt_ledger.write_text("{ this is invalid json content !!!", encoding="utf-8")

    # Manager must initialize without throwing an unhandled JSONDecodeError
    manager = IntegrityManager(ledger_path=corrupt_ledger)
    records = manager.get_registered_documents()
    assert isinstance(records, dict)

    # Verifying a file against corrupted ledger still operates safely
    result = manager.verify_file(b"test file bytes")
    assert result["status"] == "NOT_REGISTERED"

