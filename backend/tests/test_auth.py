# tests/test_auth.py

def test_signup(test_client):
    response = test_client.post(
        "/api/v1/auth/signup",
        json={"username": "testuser", "email": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login(test_client):
    response = test_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
