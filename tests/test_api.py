from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_recommend_endpoint_returns_ok():
    payload = {
        "project_name": "API Test",
        "cpu": 2,
        "ram_gb": 8,
        "gpu_required": False,
        "storage_gb": 100,
        "daily_users": 100,
        "traffic_level": "low",
        "budget": "low",
        "deployment_preference": "no_preference",
        "availability": "low",
    }

    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["project_name"] == "API Test"
    assert "recommended_architecture" in data
    assert "compute" in data["recommended_architecture"]
    assert data["confidence_score"] > 0
    assert data["estimated_monthly_cost"]["min_usd"] > 0
    assert len(data["alternatives"]) == 3
    assert data["architecture_diagram"].startswith("flowchart LR")


def test_home_page_serves_frontend():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Cloud Architecture Advisor" in response.text


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recommend_endpoint_rejects_invalid_payload():
    response = client.post(
        "/recommend",
        json={
            "project_name": "Bad Payload",
            "cpu": 0,
            "ram_gb": 8,
            "gpu_required": False,
            "storage_gb": 100,
            "daily_users": 100,
            "traffic_level": "extreme",
            "budget": "low",
            "deployment_preference": "no_preference",
            "availability": "low",
        },
    )

    assert response.status_code == 422
