"""Tests for password handler."""

import pytest

from app.infrastructure.security.password_handler import PasswordHandler


@pytest.mark.unit
def test_hash_password() -> None:
    """Test password hashing."""
    handler = PasswordHandler()
    password = "test_password_123"
    hashed = handler.hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0


@pytest.mark.unit
def test_verify_password() -> None:
    """Test password verification."""
    handler = PasswordHandler()
    password = "test_password_123"
    hashed = handler.hash_password(password)
    
    assert handler.verify_password(password, hashed) is True
    assert handler.verify_password("wrong_password", hashed) is False


