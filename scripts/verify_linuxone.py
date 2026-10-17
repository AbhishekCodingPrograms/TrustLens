"""
TrustLens LinuxONE Deep Verification Script
Theme: AI Secured - Innovation Without Exposure (IBM Z Datathon 2026)
Executes end-to-end cryptographic integrity, privacy gating, RAG grounded QA,
and audit logging against real sample documents on the local environment or remote mainframe.
"""

import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from integrity import IntegrityManager
from privacy import PrivacyScanner
from document_qa import DocumentQAPipeline
from audit import SecurityAuditor


def main():
    print("=" * 66)
    print(" TrustLens Deep Verification Run (IBM LinuxONE s390x)")
    print("=" * 66)

    test_data_dir = os.path.join(PROJECT_ROOT, "data", "test_run")
    os.makedirs(test_data_dir, exist_ok=True)

    # 1. SHA-256 Cryptographic Integrity Gate
    print("\n--- 1. SHA-256 Cryptographic Integrity Gate ---")
    ledger_path = Path(test_data_dir) / "test_ledger.json"
    integrity_mgr = IntegrityManager(ledger_path=ledger_path)

    sample_doc_path = os.path.join(PROJECT_ROOT, "sample_docs", "synthetic_financial_audit_2026.pdf")
    tampered_doc_path = os.path.join(PROJECT_ROOT, "sample_docs", "synthetic_tampered_financial_audit.pdf")

    with open(sample_doc_path, "rb") as f:
        orig_bytes = f.read()

    ref_record = integrity_mgr.register_reference(
        document_id="DOC-AUDIT-2026",
        filename="synthetic_financial_audit_2026.pdf",
        file_bytes=orig_bytes,
        notes="Baseline audited financial document"
    )
    print(f"Registered Baseline Hash : {ref_record['sha256_hash']}")

    # Verify original document against ledger
    match_result = integrity_mgr.verify_file(orig_bytes, reference_id="DOC-AUDIT-2026")
    print(f"Original Doc Verification: Status={match_result['status']}")
    print(f"Status Message           : {match_result['message']}")
    assert match_result["status"] == "MATCH", "Original document must match registered hash!"

    # Verify tampered document against ledger
    with open(tampered_doc_path, "rb") as f:
        tampered_bytes = f.read()
    tamper_result = integrity_mgr.verify_file(tampered_bytes, reference_id="DOC-AUDIT-2026")
    print(f"Tampered Doc Verification: Status={tamper_result['status']}")
    print(f"Tamper Detection Notice  : {tamper_result['message']}")
    assert tamper_result["status"] == "MODIFIED", "Tampered document must be detected as MODIFIED!"
    print("Integrity Gate Outcome   : [PASSED] Byte-level tamper detection verified.")

    # 2. Privacy Gate & Sensitive Data Redaction
    print("\n--- 2. Privacy Gate & Sensitive Data Redaction ---")
    scanner = PrivacyScanner()
    pages = scanner.extract_document(orig_bytes, "synthetic_financial_audit_2026.pdf")
    print(f"Extracted Pages          : {len(pages)} page(s) extracted")
    findings = scanner.scan(pages)
    print(f"Sensitive Data Detected  : {len(findings)} findings")
    categories = sorted(list(set(f["entity_type"] for f in findings)))
    print(f"Entity Categories        : {categories}")

    # Redact all detected findings
    redacted_pages, stats = scanner.redact_text_pages(pages, findings)
    print(f"Redactions Applied       : {stats['redactions_applied']} items masked")
    redacted_full_text = " ".join(p["text"] for p in redacted_pages)

    # Prove that raw sensitive values never appear in the redacted text
    for f in findings:
        raw_val = f["value"]
        assert raw_val not in redacted_full_text, f"CRITICAL LEAK: Raw PII '{raw_val}' found in redacted text!"
    print("Privacy Gate Outcome     : [PASSED] 100% of detected sensitive values masked.")

    # 3. Grounded QA & Model Isolation
    print("\n--- 3. Grounded QA & Model Isolation ---")
    captured_prompts = []

    def mocked_llm(prompt: str) -> str:
        captured_prompts.append(prompt)
        return "The total consulting expense is $4,850,000 for fiscal year 2026."

    qa_pipeline = DocumentQAPipeline(model_invoker=mocked_llm)
    indexed_chunks = qa_pipeline.load_document(redacted_pages, "synthetic_financial_audit_2026.pdf")
    print(f"Indexed Document Chunks  : {indexed_chunks} chunks indexed")

    # Query with sufficient evidence
    query = "What is the total consulting expense?"
    qa_result = qa_pipeline.answer_question(query)
    print(f"User Query               : '{query}'")
    print(f"Model Answer             : {qa_result['answer']}")
    print(f"Evidence Citations       : {qa_result['citations']}")
    print(f"Evidence Found Flag      : {qa_result['evidence_found']}")
    assert qa_result["evidence_found"], "Evidence must be found for consulting expense query!"
    assert len(qa_result["citations"]) > 0, "Citations must be returned with page numbers!"

    # Verify that untrusted defense wrapper is in prompt and NO sensitive PII reached the model
    assert len(captured_prompts) == 1, "Expected exactly 1 LLM invocation"
    transmitted_prompt = captured_prompts[0]
    assert "<untrusted_document_context>" in transmitted_prompt, "Context must be framed in untrusted tags."
    for f in findings:
        assert f["value"] not in transmitted_prompt, f"CRITICAL: Unmasked PII leaked to LLM prompt: {f['value']}"
    print("Model Isolation Proof    : [PASSED] Zero sensitive PII reached model prompt payload.")

    # Query with insufficient evidence (reject without hallucination)
    unsupported_query = "What was the CEO's favorite childhood book?"
    unsupported_result = qa_pipeline.answer_question(unsupported_query)
    print(f"\nUnsupported Query        : '{unsupported_query}'")
    print(f"System Response          : '{unsupported_result['answer']}'")
    print(f"Evidence Found Flag      : {unsupported_result['evidence_found']}")
    assert not unsupported_result["evidence_found"], "Unsupported query must reject without hallucinating!"
    print("Hallucination Defense    : [PASSED] Insufficient evidence properly rejected.")

    # 4. Tamper-Evident Audit Trail
    print("\n--- 4. Tamper-Evident Audit Trail ---")
    audit_log_path = Path(test_data_dir) / "test_audit.json"
    auditor = SecurityAuditor(log_path=audit_log_path)
    auditor.log_event("DOCUMENT_INGESTED", {"sha256_hash": ref_record['sha256_hash'], "actor_role": "Security Officer"})
    auditor.log_event("INTEGRITY_CHECK", {"status": match_result["status"], "actor_role": "Compliance Auditor"})
    auditor.log_event("INTEGRITY_CHECK", {"status": tamper_result["status"], "actor_role": "Compliance Auditor"})
    auditor.log_event("PRIVACY_SCAN", {"total_findings": len(findings), "actor_role": "Security Officer"})
    auditor.log_event("REDACTION_APPLIED", {"redactions_applied": stats["redactions_applied"], "actor_role": "Security Officer"})
    auditor.log_event("QA_QUERY", {"evidence_found": qa_result["evidence_found"], "latency_ms": 12.5, "actor_role": "Restricted Viewer"})
    auditor.log_event("QA_QUERY", {"evidence_found": unsupported_result["evidence_found"], "latency_ms": 8.1, "actor_role": "Restricted Viewer"})

    metrics = auditor.get_dashboard_metrics()
    print(f"Documents Processed      : {metrics['documents_processed']}")
    print(f"Sensitive Items Detected : {metrics['sensitive_items_detected']}")
    print(f"Redactions Performed     : {metrics['redactions_performed']}")
    print(f"Integrity Checks Passed  : {metrics['integrity_checks_passed']}")
    print(f"Integrity Checks Failed  : {metrics['integrity_checks_failed']}")
    print(f"Questions With Evidence  : {metrics['questions_with_evidence']}")
    print(f"Questions Insufficient   : {metrics['questions_insufficient_evidence']}")
    print(f"Average Query Latency    : {metrics['avg_latency_ms']} ms")
    assert metrics["documents_processed"] == 1
    assert metrics["integrity_checks_passed"] == 1
    assert metrics["integrity_checks_failed"] == 1
    assert metrics["questions_with_evidence"] == 1
    assert metrics["questions_insufficient_evidence"] == 1
    print("Audit Trail Outcome      : [PASSED] Real dashboard metrics computed strictly from logs.")

    # Cleanup test files
    for p in [ledger_path, audit_log_path, Path(test_data_dir)]:
        if p.exists():
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                try:
                    p.rmdir()
                except OSError:
                    pass

    print("\n" + "=" * 66)
    print(" ALL DEEP VERIFICATION CHECKS COMPLETED AND FULLY PASSED!")
    print("=" * 66)


if __name__ == "__main__":
    main()
