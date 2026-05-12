import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../app"))
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    res = client.get("/")
    assert res.status_code == 200


def test_index_has_status_field(client):
    res = client.get("/")
    data = res.get_json()
    assert data["status"] == "running"


def test_health_returns_200(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "healthy"


def test_metrics_returns_cpu(client):
    res = client.get("/metrics")
    assert res.status_code == 200
    data = res.get_json()
    assert "cpu_percent" in data
    assert "memory" in data
    assert "disk" in data


def test_ready_returns_200(client):
    res = client.get("/ready")
    assert res.status_code in [200, 503]
