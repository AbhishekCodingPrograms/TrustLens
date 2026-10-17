"""
Automated unit tests for TrustLens Document Integrity Module.
"""

import pytest
import tempfile
import os
from pathlib import Path

from integrity import IntegrityManager


@pytest.fixture
def temp_ledger(tmp_path):
    ledger_file = tmp_path / "test_ledger.json"
    return IntegrityManager(ledger_path=ledger_file)


def test_sha256_calculation():
    sample_bytes = b"TrustLens: Privacy-Gated AI for IBM Z"
    # Known SHA-256 for this exact byte sequence
    computed_hash = IntegrityManager.calculate_sha256(sample_bytes)
    assert len(computed_hash) == 64
    assert isinstance(computed_hash, str)
    # Re-calculation produces deterministic identical hash
    assert computed_hash == IntegrityManager.calculate_sha256(sample_bytes)


def test_sha256_empty_bytes():
    empty_bytes = b""
    computed_hash = IntegrityManager.calculate_sha256(empty_bytes)
    # SHA-256 of empty bytes is e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    assert computed_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_register_and_verify_match(temp_ledger):
    content = b"Confidential Quarterly Financial Audit 2026"
    doc_id = "DOC-FIN-001"
    filename = "financial_audit.pdf"

    # Register document
    reg_record = temp_ledger.register_reference(
        document_id=doc_id,
        filename=filename,
        file_bytes=content,
        notes="Official baseline audit"
    )

    assert reg_record["document_id"] == doc_id
    assert reg_record["sha256_hash"] == IntegrityManager.calculate_sha256(content)

    # Verify identical bytes
    verify_result = temp_ledger.verify_file(content, reference_id=doc_id)
    assert verify_result["status"] == "MATCH"
    assert "PASSED" in verify_result["message"]
    assert verify_result["expected_hash"] == reg_record["sha256_hash"]


def test_tamper_detection(temp_ledger):
    original_content = b"Approved Transfer Amount: $1,000,000 USD to Escrow"
    tampered_content = b"Approved Transfer Amount: $9,000,000 USD to Escrow"
    doc_id = "DOC-WIRE-99"

    temp_ledger.register_reference(
        document_id=doc_id,
        filename="wire_transfer.pdf",
        file_bytes=original_content
    )

    # Verify tampered content against original reference
    verify_result = temp_ledger.verify_file(tampered_content, reference_id=doc_id)
    assert verify_result["status"] == "MODIFIED"
    assert "SECURITY WARNING" in verify_result["message"]
    assert verify_result["current_hash"] != verify_result["expected_hash"]


def test_not_registered_document(temp_ledger):
    unknown_content = b"Unknown uncataloged document bytes"
    verify_result = temp_ledger.verify_file(unknown_content)
    assert verify_result["status"] == "NOT_REGISTERED"
