"""Unit tests for auth service functions in app/services/auth_service.py."""

import pytest
from fastapi import HTTPException

from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import create_user, authenticate_user


class TestCreateUser:
    def test_creates_user_successfully(self, db):
        user_data = UserCreate(username="alice", email="alice@example.com", password="secret123")
        response = create_user(db, user_data)
        assert response.status_code == 200
        body = response.body
        import json
        data = json.loads(body)
        assert data["username"] == "alice"
        assert data["email"] == "alice@example.com"
        assert "token" in data

    def test_duplicate_email_raises_400(self, db):
        user_data = UserCreate(username="bob", email="bob@example.com", password="pass")
        create_user(db, user_data)
        with pytest.raises(HTTPException) as exc_info:
            create_user(db, UserCreate(username="bob2", email="bob@example.com", password="pass2"))
        assert exc_info.value.status_code == 400

    def test_password_is_hashed_in_db(self, db):
        from app.models.user import User
        user_data = UserCreate(username="carol", email="carol@example.com", password="plaintext")
        create_user(db, user_data)
        db_user = db.query(User).filter(User.email == "carol@example.com").first()
        assert db_user is not None
        assert db_user.password != "plaintext"


class TestAuthenticateUser:
    def test_valid_credentials_return_token(self, db):
        import json
        create_user(db, UserCreate(username="dave", email="dave@example.com", password="mypass"))
        response = authenticate_user(db, UserLogin(email="dave@example.com", password="mypass"))
        assert response.status_code == 200
        data = json.loads(response.body)
        assert "token" in data
        assert "dave" in data["message"]

    def test_invalid_email_raises_401(self, db):
        with pytest.raises(HTTPException) as exc_info:
            authenticate_user(db, UserLogin(email="nobody@example.com", password="pass"))
        assert exc_info.value.status_code == 401

    def test_wrong_password_raises_401(self, db):
        create_user(db, UserCreate(username="eve", email="eve@example.com", password="correct"))
        with pytest.raises(HTTPException) as exc_info:
            authenticate_user(db, UserLogin(email="eve@example.com", password="wrong"))
        assert exc_info.value.status_code == 401
