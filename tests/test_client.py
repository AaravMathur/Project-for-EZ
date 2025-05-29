import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_and_email_verification():
    # Signup
    response = client.post("/client/signup", data={"email": "testuser@example.com", "password": "testpass123"})
    assert response.status_code == 200
    verification_url = response.json()["verification_url"]
    assert "token=" in verification_url

    # Extract token from URL
    token = verification_url.split("token=")[-1]

    # Email verify
    response = client.get(f"/client/email-verify?token={token}")
    assert response.status_code == 200
    assert response.json()["message"] == "Email verified"

def test_login():
    # Login after verification
    response = client.post("/client/login", data={"email": "testuser@example.com", "password": "testpass123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_list_files_requires_auth():
    # Should fail without auth
    response = client.get("/client/files")
    assert response.status_code == 401 or response.status_code == 403
