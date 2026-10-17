"""
TrustLens: Privacy-Gated AI with Verifiable Evidence
Theme: AI Secured - Innovation Without Exposure
IBM Z Datathon 2026

Interactive Streamlit Application providing Privacy Gate scanning,
SHA-256 cryptographic integrity verification, evidence-grounded document Q&A,
and tamper-evident security audit logging.
"""

import time
import io
from pathlib import Path
import streamlit as st
import pandas as pd

from config import (
    get_system_info,
    MAX_FILE_SIZE_BYTES,
    ALLOWED_EXTENSIONS,
    RAG_CONFIG,
    ROLE_PERMISSIONS
)
from integrity import IntegrityManager
from privacy import PrivacyScanner
from document_qa import DocumentQAPipeline
from audit import SecurityAuditor


# ---------------------------------------------------------
# Page Setup & Streamlit Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="TrustLens | Privacy-Gated AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Singletons
if "integrity_mgr" not in st.session_state:
    st.session_state.integrity_mgr = IntegrityManager()

if "privacy_scanner" not in st.session_state:
    st.session_state.privacy_scanner = PrivacyScanner()

if "qa_pipeline" not in st.session_state:
    st.session_state.qa_pipeline = DocumentQAPipeline()

if "auditor" not in st.session_state:
    st.session_state.auditor = SecurityAuditor()

if "uploaded_doc" not in st.session_state:
    st.session_state.uploaded_doc = None

if "doc_pages" not in st.session_state:
    st.session_state.doc_pages = []

if "scan_findings" not in st.session_state:
    st.session_state.scan_findings = []

if "redacted_pages" not in st.session_state:
    st.session_state.redacted_pages = []

if "redaction_summary" not in st.session_state:
    st.session_state.redaction_summary = {}

if "privacy_locked" not in st.session_state:
    st.session_state.privacy_locked = False

if "last_verification" not in st.session_state:
    st.session_state.last_verification = None

if "active_role" not in st.session_state:
    st.session_state.active_role = "Security Officer"


# ---------------------------------------------------------
# Custom Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 5px solid #0f62fe;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .status-badge-match {
        background-color: #defbe6;
        color: #0e6027;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
    }
    .status-badge-tamper {
        background-color: #ffebe9;
        color: #da1e28;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-protected {
        background-color: #0f62fe;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.85em;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Sidebar: System Environment & Navigation
# ---------------------------------------------------------
sys_info = get_system_info()
backends = PrivacyScanner.get_supported_backends()

with st.sidebar:
    st.title("🛡️ TrustLens")
    st.caption("**IBM Z Datathon 2026**")
    st.markdown("---")

    nav_selection = st.radio(
        "Navigation",
        [
            "📊 Security Dashboard",
            "🔐 Integrity Gate",
            "👁️ Privacy Gate & Redaction",
            "💡 Evidence-Grounded Q&A",
            "📜 Audit Ledger"
        ],
        index=0
    )

    st.markdown("---")
    st.subheader("🖥️ Platform Status")
    st.write(f"**Host OS:** {sys_info['system']}")
    st.write(f"**CPU Architecture:** `{sys_info['machine']}`")
    st.write(f"**Target Class:** {sys_info['architecture_label']}")
    st.write(f"**Python Runtime:** {sys_info['python_version']}")
    st.write(f"**PDF Engine:** `{backends['active_backend']}`")

    st.markdown("---")
    st.subheader("👤 Role-Based Access (RBAC)")
    current_role = st.selectbox(
        "Active Persona",
        options=list(ROLE_PERMISSIONS.keys()),
        index=list(ROLE_PERMISSIONS.keys()).index(st.session_state.active_role),
        help="Demonstrates separation of duties for enterprise audits."
    )
    st.session_state.active_role = current_role
    st.caption(f"_{ROLE_PERMISSIONS[current_role]['description']}_")

    st.markdown("---")
    st.caption("🔒 **Zero-Trust Policy:** By default, all document processing runs 100% locally. Original unredacted text is never transmitted to external APIs.")

perms = ROLE_PERMISSIONS[st.session_state.active_role]


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def process_uploaded_file(uploaded_file):
    """Handles file validation, hashing, text extraction, and initial privacy scan."""
    file_bytes = uploaded_file.getvalue()
    filename = uploaded_file.name

    # Validate file size
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        st.error(f"File size exceeds maximum allowed limit ({MAX_FILE_SIZE_BYTES / (1024*1024):.1f} MB).")
        return False

    # Validate file extension
    file_ext = Path(filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        st.error(f"Unsupported file format '{file_ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
        return False

    # Extract text pages
    try:
        pages = st.session_state.privacy_scanner.extract_document(file_bytes, filename)
    except Exception as e:
        st.error(f"Failed to process document: {str(e)}")
        return False

    # Calculate SHA-256
    doc_hash = IntegrityManager.calculate_sha256(file_bytes)

    # Perform Privacy Scan
    findings = st.session_state.privacy_scanner.scan(pages)

    # Save to session state
    st.session_state.uploaded_doc = {
        "filename": filename,
        "bytes": file_bytes,
        "hash": doc_hash,
        "size": len(file_bytes)
    }
    st.session_state.doc_pages = pages
    st.session_state.scan_findings = findings
    st.session_state.redacted_pages = []
    st.session_state.redaction_summary = {}
    st.session_state.privacy_locked = False
    st.session_state.last_verification = None
    st.session_state.qa_pipeline = DocumentQAPipeline()

    # Log ingestion audit event
    st.session_state.auditor.log_event("DOCUMENT_INGESTED", {
        "filename": filename,
        "sha256_hash": doc_hash,
        "file_size_bytes": len(file_bytes),
        "pages_count": len(pages)
    })

    st.session_state.auditor.log_event("PRIVACY_SCAN", {
        "filename": filename,
        "total_findings": len(findings),
        "entities_detected": list({f["entity_type"] for f in findings})
    })

    return True


# =========================================================
# Page 1: Security Dashboard
# =========================================================
if nav_selection == "📊 Security Dashboard":
    st.header("📊 Real-Time Security & Compliance Dashboard")
    st.markdown("Continuous operational metrics tracked across ingestion, integrity verification, privacy controls, and grounded AI retrieval.")

    metrics = st.session_state.auditor.get_dashboard_metrics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Documents Ingested", metrics["documents_processed"])
    with col2:
        st.metric("Sensitive Items Detected", metrics["sensitive_items_detected"])
    with col3:
        st.metric("Redactions Enforced", metrics["redactions_performed"])
    with col4:
        st.metric("Integrity Checks Passed", metrics["integrity_checks_passed"])

    st.markdown("---")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Integrity Tamper Alerts", metrics["integrity_checks_failed"], delta_color="inverse")
    with col6:
        st.metric("Q&A with Verifiable Evidence", metrics["questions_with_evidence"])
    with col7:
        st.metric("Unsupported Inquiries Rejected", metrics["questions_insufficient_evidence"])
    with col8:
        st.metric("Avg Retrieval Latency", f"{metrics['avg_latency_ms']} ms")

    st.markdown("---")
    st.subheader("🛡️ Active Privacy & Execution Status")
    if st.session_state.uploaded_doc:
        doc = st.session_state.uploaded_doc
        st.success(f"**Loaded Document:** `{doc['filename']}` | **Size:** {doc['size']:,} bytes | **SHA-256:** `{doc['hash'][:16]}...`")
        if st.session_state.privacy_locked:
            st.info("🔒 **AI Isolation Status:** Active. AI pipeline is strictly isolated using approved redacted text.")
        else:
            st.warning("⚠️ **AI Isolation Status:** Document uploaded but NOT yet approved in Privacy Gate. Proceed to 'Privacy Gate & Redaction'.")
    else:
        st.info("No document currently loaded. Upload a document in **Integrity Gate** or **Privacy Gate** to begin.")


# =========================================================
# Page 2: Integrity Gate
# =========================================================
elif nav_selection == "🔐 Integrity Gate":
    st.header("🔐 Document Cryptographic Integrity Gate")
    st.markdown("""
    Calculate byte-level **SHA-256 cryptographic hashes**, register trusted baseline records,
    and detect unauthorized document tampering before AI ingestion.
    """)

    uploaded_file = st.file_uploader("Upload PDF or TXT Document for Integrity Verification", type=["pdf", "txt"], key="integrity_uploader")

    if uploaded_file:
        if not st.session_state.uploaded_doc or st.session_state.uploaded_doc["filename"] != uploaded_file.name:
            if process_uploaded_file(uploaded_file):
                st.rerun()

    if st.session_state.uploaded_doc:
        doc = st.session_state.uploaded_doc
        file_bytes = doc["bytes"]
        computed_hash = doc["hash"]

        st.subheader("1. Cryptographic Fingerprint")
        st.code(f"SHA-256: {computed_hash}", language="text")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Baseline Reference Registration")
            doc_id_input = st.text_input("Document Identifier", value=f"DOC-{doc['filename'].split('.')[0].upper()[:12]}")
            reg_notes = st.text_area("Audit Notes", value="Baseline registered for IBM Z Datathon 2026 verification.")

            if perms["can_register_baseline"]:
                if st.button("📝 Register as Reference Baseline", type="primary"):
                    reg_record = st.session_state.integrity_mgr.register_reference(
                        document_id=doc_id_input,
                        filename=doc["filename"],
                        file_bytes=file_bytes,
                        notes=reg_notes
                    )
                    st.session_state.auditor.log_event("INTEGRITY_REGISTERED", {
                        "document_id": doc_id_input,
                        "sha256_hash": computed_hash,
                        "filename": doc["filename"]
                    })
                    st.success(f"Registered reference for `{doc_id_input}`.")
                    st.rerun()
            else:
                st.button("📝 Register as Reference Baseline", disabled=True, help="Requires Security Officer role")
                st.caption("🔒 *Registration restricted: Requires 'Security Officer' role.*")

        with col2:
            st.markdown("#### Tamper & Modification Check")
            registered_docs = st.session_state.integrity_mgr.get_registered_documents()
            ref_options = ["(Auto-Detect by Hash)"] + list(registered_docs.keys())

            selected_ref = st.selectbox("Compare Against Registered Baseline", ref_options)

            if perms["can_verify_integrity"]:
                if st.button("🔍 Verify Integrity Against Baseline"):
                    target_ref_id = None if selected_ref == "(Auto-Detect by Hash)" else selected_ref
                    result = st.session_state.integrity_mgr.verify_file(
                        file_bytes=file_bytes,
                        reference_id=target_ref_id,
                        filename=doc["filename"]
                    )
                    st.session_state.last_verification = result
                    st.session_state.auditor.log_event("INTEGRITY_CHECK", result)
            else:
                st.button("🔍 Verify Integrity Against Baseline", disabled=True, help="Requires Compliance Auditor or Security Officer role")
                st.caption("🔒 *Verification restricted: Requires 'Compliance Auditor' or 'Security Officer' role.*")

        if st.session_state.last_verification:
            res = st.session_state.last_verification
            st.markdown("---")
            if res["status"] == "MATCH":
                st.success(f"✅ **INTEGRITY CHECK PASSED (MATCH):** {res['message']}")
            elif res["status"] == "MODIFIED":
                st.error(f"🚨 **SECURITY ALERT (MODIFIED):** {res['message']}")
            else:
                st.warning(f"ℹ️ **STATUS:** {res['message']}")

            st.caption(f"**Disclaimer:** {res['disclaimer']}")

        st.markdown("---")
        st.subheader("📚 Registered Baseline Reference Ledger")
        registered_records = st.session_state.integrity_mgr.get_registered_documents()
        if registered_records:
            ledger_table = [
                {
                    "Document ID": d["document_id"],
                    "Filename": d["filename"],
                    "SHA-256 Hash": f"{d['sha256_hash'][:20]}...",
                    "Registered (UTC)": d["registered_at"],
                    "Size (bytes)": d["file_size_bytes"],
                    "Verifications": d.get("verification_count", 0)
                }
                for d in registered_records.values()
            ]
            st.dataframe(pd.DataFrame(ledger_table), use_container_width=True)
        else:
            st.caption("No baseline documents registered yet.")


# =========================================================
# Page 3: Privacy Gate & Redaction
# =========================================================
elif nav_selection == "👁️ Privacy Gate & Redaction":
    st.header("👁️ Privacy Gate: Detection & Selective Redaction")
    st.markdown("""
    Scan uploaded documents for **Emails, Phone Numbers, Tax IDs, Credit Cards, Secrets, and IP Addresses**.
    Review findings, approve redactions, and lock the sanitized document representation for AI processing.
    """)

    uploaded_file = st.file_uploader("Upload PDF or TXT Document", type=["pdf", "txt"], key="privacy_uploader")

    if uploaded_file:
        if not st.session_state.uploaded_doc or st.session_state.uploaded_doc["filename"] != uploaded_file.name:
            if process_uploaded_file(uploaded_file):
                st.rerun()

    if not st.session_state.uploaded_doc:
        st.info("Please upload a document to run the Privacy Gate scanner.")
        st.markdown("**Or load a sample synthetic document:**")
        sample_col1, sample_col2, sample_col3 = st.columns(3)
        with sample_col1:
            if st.button("📄 Load Synthetic Financial Audit"):
                sample_path = Path("sample_docs/synthetic_financial_audit_2026.pdf")
                if sample_path.exists():
                    with open(sample_path, "rb") as f:
                        class DummyFile:
                            def __init__(self, name, data):
                                self.name = name
                                self._data = data
                            def getvalue(self):
                                return self._data
                        process_uploaded_file(DummyFile("synthetic_financial_audit_2026.pdf", f.read()))
                        st.rerun()
        with sample_col2:
            if st.button("📄 Load Tampered Financial Audit"):
                sample_path = Path("sample_docs/synthetic_tampered_financial_audit.pdf")
                if sample_path.exists():
                    with open(sample_path, "rb") as f:
                        class DummyFile:
                            def __init__(self, name, data):
                                self.name = name
                                self._data = data
                            def getvalue(self):
                                return self._data
                        process_uploaded_file(DummyFile("synthetic_tampered_financial_audit.pdf", f.read()))
                        st.rerun()
        with sample_col3:
            if st.button("📄 Load Synthetic Medical Trial"):
                sample_path = Path("sample_docs/synthetic_medical_trial.pdf")
                if sample_path.exists():
                    with open(sample_path, "rb") as f:
                        class DummyFile:
                            def __init__(self, name, data):
                                self.name = name
                                self._data = data
                            def getvalue(self):
                                return self._data
                        process_uploaded_file(DummyFile("synthetic_medical_trial.pdf", f.read()))
                        st.rerun()

    else:
        findings = st.session_state.scan_findings
        doc = st.session_state.uploaded_doc

        st.subheader(f"1. Findings Detected in `{doc['filename']}` ({len(findings)} items)")

        if findings:
            finding_df = pd.DataFrame([
                {
                    "Select": True,
                    "ID": f["finding_id"],
                    "Category": f["entity_name"],
                    "Masked Value": f["masked_preview"],
                    "Page": f["page"],
                    "Context Excerpt": f["context_snippet"],
                    "Replacement Token": f["redacted_token"]
                }
                for f in findings
            ])

            # Interactive data editor for selective redaction
            edited_df = st.data_editor(
                finding_df,
                column_config={"Select": st.column_config.CheckboxColumn("Redact?", default=True)},
                disabled=["ID", "Category", "Masked Value", "Page", "Context Excerpt", "Replacement Token"],
                hide_index=True,
                use_container_width=True
            )

            # Selected finding IDs
            selected_ids = [
                edited_df.iloc[i]["ID"]
                for i in range(len(edited_df))
                if edited_df.iloc[i]["Select"]
            ]

            col1, col2 = st.columns(2)
            with col1:
                if perms["can_approve_redactions"]:
                    if st.button("🔒 Approve Redactions & Lock for AI Processing", type="primary"):
                        redacted_pages, summary = st.session_state.privacy_scanner.redact_text_pages(
                            st.session_state.doc_pages,
                            findings,
                            approved_finding_ids=selected_ids
                        )
                        st.session_state.redacted_pages = redacted_pages
                        st.session_state.redaction_summary = summary
                        st.session_state.privacy_locked = True

                        # Load ONLY redacted pages into the QA RAG Pipeline
                        num_chunks = st.session_state.qa_pipeline.load_document(
                            pages=redacted_pages,
                            source_filename=doc["filename"],
                            privacy_approved=True
                        )

                        # Log Redaction event
                        st.session_state.auditor.log_event("REDACTION_APPLIED", {
                            "filename": doc["filename"],
                            "redactions_applied": summary["redactions_applied"],
                            "items_preserved": summary["items_preserved"],
                            "categories": summary["categories_redacted"],
                            "chunks_indexed": num_chunks
                        })
                        st.success(f"Applied {summary['redactions_applied']} redactions! Document locked and {num_chunks} chunks indexed for Q&A.")
                        st.rerun()
                else:
                    st.button("🔒 Approve Redactions & Lock for AI Processing", disabled=True, help="Requires Security Officer role")
                    st.caption("🔒 *Redaction approval restricted: Requires 'Security Officer' role.*")

            with col2:
                # Option to download verified redacted PDF
                if doc["filename"].lower().endswith(".pdf"):
                    if perms["can_download_sanitized_pdf"]:
                        redacted_pdf_bytes, method_note = st.session_state.privacy_scanner.redact_pdf_bytes(
                            doc["bytes"],
                            findings,
                            approved_finding_ids=selected_ids
                        )
                        st.download_button(
                            label="📥 Download Sanitized PDF",
                            data=redacted_pdf_bytes,
                            file_name=f"sanitized_{doc['filename']}",
                            mime="application/pdf",
                            help=f"Redaction Engine: {method_note}"
                        )
                    else:
                        st.caption("🔒 *PDF export restricted to 'Security Officer' role.*")
        else:
            st.success("No sensitive PII or credentials detected in this document.")
            if perms["can_approve_redactions"]:
                if st.button("✅ Approve Unredacted Document for AI Processing", type="primary"):
                    st.session_state.redacted_pages = st.session_state.doc_pages
                    st.session_state.privacy_locked = True
                    num_chunks = st.session_state.qa_pipeline.load_document(
                        pages=st.session_state.doc_pages,
                        source_filename=doc["filename"],
                        privacy_approved=True
                    )
                    st.success(f"Document approved and {num_chunks} chunks indexed for Q&A.")
                    st.rerun()
            else:
                st.caption("🔒 *Approval restricted: Requires 'Security Officer' role.*")

        # Display side-by-side comparison if locked
        if st.session_state.privacy_locked:
            st.markdown("---")
            st.subheader("2. Sanitized Document Inspection (AI-Approved View)")
            tab_redacted, tab_original = st.tabs(["🔒 Approved Redacted Text (AI Pipeline Input)", "📄 Original Raw Text (Restricted)"])

            with tab_redacted:
                for p in st.session_state.redacted_pages:
                    st.markdown(f"**--- Page {p['page']} ---**")
                    st.text(p["text"])

            with tab_original:
                st.warning("⚠️ Restricted View: This raw text is BLOCKED from reaching the AI model.")
                for p in st.session_state.doc_pages:
                    st.markdown(f"**--- Page {p['page']} ---**")
                    st.text(p["text"])


# =========================================================
# Page 4: Evidence-Grounded Q&A
# =========================================================
elif nav_selection == "💡 Evidence-Grounded Q&A":
    st.header("💡 Evidence-Grounded Document Q&A (RAG)")
    st.markdown("""
    Ask questions against the approved document. The pipeline retrieves verifiable evidence passages,
    cites exact page numbers, and **strictly rejects questions when sufficient evidence is missing**.
    """)

    if not st.session_state.privacy_locked:
        st.warning("⚠️ Privacy Gate Approval Required: You must first inspect and approve the document redactions in the **'Privacy Gate & Redaction'** tab.")
    else:
        st.success(f"🔒 **Protected AI Pipeline Active:** Reading from sanitized representation of `{st.session_state.uploaded_doc['filename']}`.")

        # Quick sample question buttons
        st.markdown("**Sample Inquiries for Ingested Documents:**")
        qcol1, qcol2, qcol3 = st.columns(3)
        sample_q = ""
        with qcol1:
            if st.button("❓ What is the settlement or reserve amount?"):
                sample_q = "What is the settlement or reserve amount?"
        with qcol2:
            if st.button("❓ Who is the auditor or investigator?"):
                sample_q = "Who is the auditor or investigator?"
        with qcol3:
            if st.button("❓ Unsupported: What is the Mars orbital speed?"):
                sample_q = "What is the Mars orbital speed?"

        question_input = st.text_input("Enter your question:", value=sample_q, key="qa_query_input")

        if st.button("🔎 Submit Grounded Query", type="primary") or question_input:
            if question_input.strip():
                with st.spinner("Retrieving evidence passages and synthesizing grounded response..."):
                    result = st.session_state.qa_pipeline.answer_question(question_input)

                    # Log Query Audit Event
                    st.session_state.auditor.log_event("QA_QUERY", {
                        "question": question_input,
                        "evidence_found": result["evidence_found"],
                        "citations": result.get("citations", []),
                        "latency_ms": result["latency_ms"],
                        "model_used": result["model_used"]
                    })

                # Display Results
                st.markdown("---")
                col_ans, col_meta = st.columns([3, 1])

                with col_ans:
                    if result["evidence_found"]:
                        st.success("✅ **Verified with Verifiable Document Evidence**")
                        st.markdown(result["answer"])

                        st.markdown("#### 📖 Exact Page Citations")
                        for citation in result["citations"]:
                            st.badge = st.markdown(f"- 🏷️ `{citation}`")

                        st.markdown("#### 📑 Supporting Verbatim Excerpts")
                        for idx, passage in enumerate(result["supporting_passages"]):
                            with st.expander(f"Evidence Excerpt {idx+1} [Page {passage['page']} | Relevance: {passage['relevance_score']}]"):
                                st.write(passage["text"])
                    else:
                        st.error("🚫 **Insufficient Evidence in Approved Document**")
                        st.markdown(result["answer"])
                        st.info("The AI pipeline refuses to hallucinate facts not present in the verified document content.")

                with col_meta:
                    st.markdown("#### Operational Metadata")
                    st.metric("Query Latency", f"{result['latency_ms']} ms")
                    st.write(f"**Inference Engine:** `{result['model_used']}`")
                    st.write("**Data Transmission:** `0 bytes (100% Local)`")
                    st.write(f"**Indexed Chunks:** {len(st.session_state.qa_pipeline.retriever.chunks)}")


# =========================================================
# Page 5: Audit Ledger
# =========================================================
elif nav_selection == "📜 Audit Ledger":
    st.header("📜 Tamper-Evident Security Audit Ledger")
    st.markdown("Immutable record of all document events, privacy scans, redactions, integrity checks, and user inquiries.")

    if not perms["can_view_audit"]:
        st.error(f"🚫 **Access Restricted:** The active persona `{st.session_state.active_role}` lacks clearance to view the security audit ledger.")
        st.info("Switch to **'Security Officer'** or **'Compliance Auditor'** in the sidebar to inspect audit events.")
    else:
        events = st.session_state.auditor.get_events(limit=50)

        if events:
            table_rows = []
            for e in events:
                details_str = ", ".join([f"{k}: {v}" for k, v in e.get("details", {}).items() if not isinstance(v, (list, dict))])
                table_rows.append({
                    "Timestamp (UTC)": e["timestamp"],
                    "Event Type": e["event_type"],
                    "Details": details_str
                })

            st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

            # Export audit trail button
            if perms["can_export_audit"]:
                audit_json = st.session_state.auditor._load_data()
                st.download_button(
                    label="📥 Export Full Audit Trail (JSON)",
                    data=pd.Series(audit_json).to_json(indent=2),
                    file_name="trustlens_audit_trail.json",
                    mime="application/json"
                )
            else:
                st.caption("🔒 *Audit export restricted to Compliance Auditor and Security Officer roles.*")
        else:
            st.info("No audit events recorded yet.")
