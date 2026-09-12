from fastapi.testclient import TestClient

from geopulse.api.fastapi.app import app

client = TestClient(app)


def test_health_live_returns_exact_status() -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_ready_returns_ready() -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
