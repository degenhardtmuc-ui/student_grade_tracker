"""Tests for the Student Grade Tracker REST API."""

"""Tests for the Student Grade Tracker REST API."""

import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import notenverwaltung.api as api_module
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
def test_get_students(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The students endpoint should return data from SQLite."""

    test_database = tmp_path / "test_grade_tracker.db"

    with sqlite3.connect(test_database) as connection:
        connection.execute(
            """
            CREATE TABLE students (
                student_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )

        connection.executemany(
            """
            INSERT INTO students (
                student_id,
                first_name,
                last_name,
                email
            )
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    "S001",
                    "Anna",
                    "Schmidt",
                    "anna@example.com",
                ),
                (
                    "S002",
                    "Daniel",
                    "Degenhardt",
                    "daniel@example.com",
                ),
            ],
        )

    monkeypatch.setattr(
        api_module,
        "DATABASE_PATH",
        test_database,
    )

    response = client.get("/students")

    assert response.status_code == 200
    assert response.json() == [
        {
            "student_id": "S001",
            "first_name": "Anna",
            "last_name": "Schmidt",
        },
        {
            "student_id": "S002",
            "first_name": "Daniel",
            "last_name": "Degenhardt",
        },
    ]