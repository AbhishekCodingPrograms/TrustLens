"""
Automated unit tests for TrustLens Privacy Gate Module.
"""

import pytest
import io
from fpdf import FPDF
from privacy import PrivacyScanner


@pytest.fixture
def scanner():
    return PrivacyScanner()


def test_email_and_phone_detection(scanner):
    sample_text = (
        "Please reach out to Alice Johnson at alice.johnson@enterprise-bank.com "
        "or call her direct mobile line at +1 (555) 234-5678 regarding loan #9921."
    )
    pages = [{"page": 1, "text": sample_text}]

    findings = scanner.scan(pages)
    detected_types = {f["entity_type"] for f in findings}

    assert "EMAIL" in detected_types
    assert "PHONE_NUMBER" in detected_types

    email_finding = next(f for f in findings if f["entity_type"] == "EMAIL")
    assert email_finding["value"] == "alice.johnson@enterprise-bank.com"
    assert email_finding["page"] == 1
    assert "alice.johnson" in email_finding["context_snippet"]


def test_credit_card_and_ssn_detection(scanner):
    sample_text = (
        "Primary cardholder SSN is 452-89-1234. Card number 4111111111111111 "
        "was charged for transaction verification."
    )
    pages = [{"page": 1, "text": sample_text}]

    findings = scanner.scan(pages)
    detected_types = {f["entity_type"] for f in findings}

    assert "SSN_TAX_ID" in detected_types
    assert "CREDIT_CARD" in detected_types


def test_redaction_behavior(scanner):
    sample_text = (
        "Executive contact: john.doe@ibm.com, phone 555-890-1234. Internal server IP 192.168.1.105."
    )
    pages = [{"page": 1, "text": sample_text}]

    findings = scanner.scan(pages)
    assert len(findings) >= 3

    # Redact ALL
    redacted_pages, summary = scanner.redact_text_pages(pages, findings)

    redacted_text = redacted_pages[0]["text"]
    assert "john.doe@ibm.com" not in redacted_text
    assert "555-890-1234" not in redacted_text
    assert "192.168.1.105" not in redacted_text
    assert "[REDACTED_EMAIL_" in redacted_text
    assert summary["redactions_applied"] >= 3
    assert summary["items_preserved"] == 0


def test_selective_redaction(scanner):
    sample_text = "Contact alice@corp.com or bob@partner.org."
    pages = [{"page": 1, "text": sample_text}]

    findings = scanner.scan(pages)
    assert len(findings) == 2

    # User decides to only redact Alice's email
    alice_id = next(f["finding_id"] for f in findings if "alice" in f["value"])
    redacted_pages, summary = scanner.redact_text_pages(
        pages, findings, approved_finding_ids=[alice_id]
    )

    redacted_text = redacted_pages[0]["text"]
    assert "alice@corp.com" not in redacted_text
    assert "bob@partner.org" in redacted_text  # Preserved as user requested
    assert summary["redactions_applied"] == 1
    assert summary["items_preserved"] == 1


def test_pdf_extraction_and_redaction(scanner):
    # Dynamically generate a valid synthetic test PDF using pure-Python fpdf2
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    pdf.cell(text="CONFIDENTIAL REPORT - Page 1. Lead Analyst: sarah.smith@acme.org")
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    pdf.cell(text="CONFIDENTIAL REPORT - Page 2. Support line: 800-555-0199")

    pdf_bytes = bytes(pdf.output())

    # Extract pages
    extracted_pages = scanner.extract_document(pdf_bytes, "test.pdf")
    assert len(extracted_pages) == 2
    assert extracted_pages[0]["page"] == 1
    assert "sarah.smith@acme.org" in extracted_pages[0]["text"]
    assert extracted_pages[1]["page"] == 2
    assert "800-555-0199" in extracted_pages[1]["text"]

    # Scan
    findings = scanner.scan(extracted_pages)
    assert len(findings) == 2
    assert findings[0]["page"] == 1
    assert findings[1]["page"] == 2

    # Verify redacted text pages
    redacted_pages, summary = scanner.redact_text_pages(extracted_pages, findings)
    assert "sarah.smith@acme.org" not in redacted_pages[0]["text"]
    assert "800-555-0199" not in redacted_pages[1]["text"]
    assert summary["redactions_applied"] == 2
