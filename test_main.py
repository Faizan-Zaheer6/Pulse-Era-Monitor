from fastapi.testclient import TestClient
from main import app  # Aapki main file se app ko import karega

client = TestClient(app)

def test_home_route():
    """Check karein ke Home route sahi chal raha hai"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Pulse Era API is Running"

def test_status_route():
    """Check karein ke status list format mein hai"""
    response = client.get("/status")
    assert response.status_code == 200
    assert isinstance(response.json(), list)