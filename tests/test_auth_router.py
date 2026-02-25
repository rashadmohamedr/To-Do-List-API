"""Integration tests for authentication endpoints (/auth/signup and /auth/login)."""

import pytest


class TestSignup:
    def test_signup_success(self, client):
        response = client.post("/auth/signup", json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret123",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "alice"
        assert data["email"] == "alice@example.com"
        assert "token" in data
        assert data["message"] == "User created successfully"

    def test_signup_duplicate_email_returns_400(self, client):
        payload = {"username": "bob", "email": "bob@example.com", "password": "pass"}
        client.post("/auth/signup", json=payload)
        response = client.post("/auth/signup", json={
            "username": "bob2",
            "email": "bob@example.com",
            "password": "pass2",
        })
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_signup_missing_fields_returns_422(self, client):
        response = client.post("/auth/signup", json={"username": "incomplete"})
        assert response.status_code == 422

    def test_signup_invalid_email_returns_422(self, client):
        response = client.post("/auth/signup", json={
            "username": "carol",
            "email": "not-an-email",
            "password": "pass",
        })
        assert response.status_code == 422


class TestLogin:
    def _register(self, client, username, email, password):
        client.post("/auth/signup", json={
            "username": username,
            "email": email,
            "password": password,
        })

    def test_login_success(self, client):
        self._register(client, "dave", "dave@example.com", "mypass")
        response = client.post("/auth/login", json={
            "email": "dave@example.com",
            "password": "mypass",
        })
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "dave" in data["message"]

    def test_login_wrong_password_returns_401(self, client):
        self._register(client, "eve", "eve@example.com", "correct")
        response = client.post("/auth/login", json={
            "email": "eve@example.com",
            "password": "wrong",
        })
        assert response.status_code == 401

    def test_login_unknown_email_returns_401(self, client):
        response = client.post("/auth/login", json={
            "email": "ghost@example.com",
            "password": "pass",
        })
        assert response.status_code == 401

    def test_login_missing_fields_returns_422(self, client):
        response = client.post("/auth/login", json={"email": "incomplete@example.com"})
        assert response.status_code == 422
