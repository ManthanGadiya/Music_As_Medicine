from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_invalid_user():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "unknown@mail.com", "password": "password123"},
    )
    assert response.status_code == 401
