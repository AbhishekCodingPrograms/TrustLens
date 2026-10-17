"""
Unit tests for TrustLens Role-Based Access Control (RBAC) permissions.
Verifies separation of duties across Security Officer, Compliance Auditor, and Restricted Viewer roles.
"""

import pytest
from config import ROLE_PERMISSIONS


def test_role_definitions_exist():
    """Verify all 3 core personas are defined."""
    assert "Security Officer" in ROLE_PERMISSIONS
    assert "Compliance Auditor" in ROLE_PERMISSIONS
    assert "Restricted Viewer" in ROLE_PERMISSIONS


def test_security_officer_permissions():
    """Security Officer must possess full administrative authorization."""
    perms = ROLE_PERMISSIONS["Security Officer"]
    assert perms["can_register_baseline"] is True
    assert perms["can_verify_integrity"] is True
    assert perms["can_approve_redactions"] is True
    assert perms["can_download_sanitized_pdf"] is True
    assert perms["can_query_qa"] is True
    assert perms["can_view_audit"] is True
    assert perms["can_export_audit"] is True


def test_compliance_auditor_permissions():
    """Compliance Auditor can verify and audit, but cannot approve redactions or register baselines."""
    perms = ROLE_PERMISSIONS["Compliance Auditor"]
    assert perms["can_register_baseline"] is False
    assert perms["can_verify_integrity"] is True
    assert perms["can_approve_redactions"] is False
    assert perms["can_download_sanitized_pdf"] is False
    assert perms["can_query_qa"] is True
    assert perms["can_view_audit"] is True
    assert perms["can_export_audit"] is True


def test_restricted_viewer_permissions():
    """Restricted Viewer can only query Q&A and view dashboard, without access to audit ledger or controls."""
    perms = ROLE_PERMISSIONS["Restricted Viewer"]
    assert perms["can_register_baseline"] is False
    assert perms["can_verify_integrity"] is False
    assert perms["can_approve_redactions"] is False
    assert perms["can_download_sanitized_pdf"] is False
    assert perms["can_query_qa"] is True
    assert perms["can_view_audit"] is False
    assert perms["can_export_audit"] is False
