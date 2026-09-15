from fastapi.testclient import TestClient


def test_root_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "env" in payload
    assert "service" in payload


def test_versioned_health_returns_ok(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_api_v1_prefix_exposes_info(client: TestClient) -> None:
    response = client.get("/api/v1/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["version"] == "v1"
    assert "name" in payload
