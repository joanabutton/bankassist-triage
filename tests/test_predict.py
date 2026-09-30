from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_prediction():

    response = client.post(
        "/predict",
        json={
            "message": "I have a problem with my card"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "intent" in data
    assert "confidence" in data
    assert "route" in data
