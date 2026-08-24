"""Tests for the Student Grade Tracker REST API."""

from fastapi.testclient import TestClient

from notenverwaltung.api import app


client = TestClient(app)


def test_health_check() -> None:
    """The health endpoint should confirm that the API is running."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "student-grade-tracker-api",
    }