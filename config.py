"""
TrustLens Configuration Module
Defines privacy patterns, system architecture detection,
storage paths, and runtime settings for IBM LinuxONE compatibility.
"""

import os
import platform
import re
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)

INTEGRITY_LEDGER_PATH = DATA_DIR / "integrity_ledger.json"
AUDIT_LOG_PATH = DATA_DIR / "audit_log.json"

# System Architecture & Environment Details
def get_system_info() -> dict:
    """Detects system architecture and runtime environment."""
    machine = platform.machine().lower()
    system = platform.system()
    python_ver = platform.python_version()
    
    is_linuxone = "s390x" in machine or "s390" in machine
    
    return {
        "machine": machine,
        "system": system,
        "python_version": python_ver,
        "is_linuxone": is_linuxone,
        "platform_description": f"{system} ({machine}) - Python {python_ver}",
        "architecture_label": "IBM LinuxONE (s390x)" if is_linuxone else f"Standard ({machine})"
    }

# Sensitive Data Detection Patterns
SENSITIVE_PATTERNS = {
    "EMAIL": {
        "name": "Email Address",
        "pattern": re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,24}\b',
            re.IGNORECASE
        ),
        "description": "Standard email address format",
        "placeholder_prefix": "EMAIL"
    },
    "PHONE_NUMBER": {
        "name": "Phone Number",
        "pattern": re.compile(
            r'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?|(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+91[-.\s]?[6-9]\d{9}',
            re.IGNORECASE
        ),
        "description": "US, International, and Indian phone numbers",
        "placeholder_prefix": "PHONE"
    },
    "CREDIT_CARD": {
        "name": "Credit Card Number",
        "pattern": re.compile(
            r'\b(?:4[0-9]{3}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}|4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{2}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}|3[47][0-9]{2}[- ]?[0-9]{6}[- ]?[0-9]{5}|(?:2131|1800|35\d{3})\d{11})\b'
        ),
        "description": "Major credit card numbers (Visa, MC, Amex, Discover)",
        "placeholder_prefix": "CREDIT_CARD"
    },
    "SSN_TAX_ID": {
        "name": "SSN / National ID",
        "pattern": re.compile(
            r'\b(?!000|666|9\d{2})([0-8]\d{2})[- ](?!00)(\d{2})[- ](?!0000)(\d{4})\b'
        ),
        "description": "Social Security / National Tax Identifier (XXX-XX-XXXX)",
        "placeholder_prefix": "SSN"
    },
    "API_KEY_SECRET": {
        "name": "API Key / Secret Token",
        "pattern": re.compile(
            r'(?i)\b(?:api[_-]?key|access[_-]?token|secret[_-]?key|bearer)\s*[:=]\s*["\']?([A-Za-z0-9_\-]{16,64})["\']?|\b(sk-[a-zA-Z0-9]{20,48})\b'
        ),
        "description": "API keys, access tokens, and secret credentials",
        "placeholder_prefix": "API_KEY"
    },
    "IP_ADDRESS": {
        "name": "IP Address",
        "pattern": re.compile(
            r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        ),
        "description": "IPv4 Network addresses",
        "placeholder_prefix": "IP_ADDR"
    }
}

# RAG & Retrieval Defaults
RAG_CONFIG = {
    "chunk_size": 400,          # Words per chunk for balanced context
    "chunk_overlap": 80,        # Words overlap between consecutive chunks
    "top_k": 3,                 # Number of evidence chunks to retrieve
    "relevance_threshold": 0.15,# Minimum cosine/similarity score to consider evidence
    "default_model": "local_grounded",
    "allow_external_ai": False  # Zero-trust: default to NO external calls without authorization
}

# Max upload size (10 MB)
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".txt"}

# Role-Based Access Control (RBAC) demonstration definitions
ROLE_PERMISSIONS = {
    "Security Officer": {
        "description": "Full administrative privileges: Baseline registration, redaction approval, sanitized PDF export, and audit export.",
        "can_register_baseline": True,
        "can_verify_integrity": True,
        "can_approve_redactions": True,
        "can_download_sanitized_pdf": True,
        "can_query_qa": True,
        "can_view_audit": True,
        "can_export_audit": True,
    },
    "Compliance Auditor": {
        "description": "Audit and integrity verification: Verify SHA-256 hashes, review compliance metrics, and export audit trails.",
        "can_register_baseline": False,
        "can_verify_integrity": True,
        "can_approve_redactions": False,
        "can_download_sanitized_pdf": False,
        "can_query_qa": True,
        "can_view_audit": True,
        "can_export_audit": True,
    },
    "Restricted Viewer": {
        "description": "Restricted read-only access: View dashboard metrics and submit Q&A queries against approved documents only.",
        "can_register_baseline": False,
        "can_verify_integrity": False,
        "can_approve_redactions": False,
        "can_download_sanitized_pdf": False,
        "can_query_qa": True,
        "can_view_audit": False,
        "can_export_audit": False,
    }
}

