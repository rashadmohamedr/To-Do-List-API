"""Unit tests for JWT utility functions in app/core/jwt.py."""

from datetime import timedelta

import pytest

from app.core.jwt import create_token, verify_token, create_access_token


class TestCreateAccessToken:
    def test_returns_string(self):
        token = create_access_token({"sub": "1", "username": "alice"})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_custom_expiry(self):
        token = create_access_token({"sub": "1"}, expires_delta=timedelta(minutes=5))
        payload = verify_token(token)
        assert payload is not None
        assert "exp" in payload


class TestCreateToken:
    def test_returns_decodable_token(self):
        token = create_token(user_id=42, username="alice")
        payload = verify_token(token)
        assert payload is not None

    def test_payload_contains_expected_fields(self):
        token = create_token(user_id=7, username="bob")
        payload = verify_token(token)
        assert payload["sub"] == "7"
        assert payload["username"] == "bob"

    def test_custom_expiry(self):
        token = create_token(user_id=1, username="carol", expires_delta=timedelta(hours=1))
        payload = verify_token(token)
        assert payload is not None


class TestVerifyToken:
    def test_valid_token(self):
        token = create_token(user_id=1, username="dave")
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "1"

    def test_invalid_token_returns_none(self):
        result = verify_token("not.a.valid.token")
        assert result is None

    def test_tampered_token_returns_none(self):
        token = create_token(user_id=1, username="eve")
        tampered = token[:-5] + "xxxxx"
        assert verify_token(tampered) is None

    def test_expired_token_returns_none(self):
        token = create_access_token({"sub": "1"}, expires_delta=timedelta(seconds=-1))
        assert verify_token(token) is None
