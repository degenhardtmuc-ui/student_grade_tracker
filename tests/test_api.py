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

@pytest.fixture

def student_api_database(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """Create a temporary student database for API tests."""

    test_database = tmp_path / "student_api.db"

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

        connection.execute(
            """
            INSERT INTO students (
                student_id,
                first_name,
                last_name,
                email
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "S002",
                "Daniel",
                "Degenhardt",
                "daniel@example.com",
            ),
        )

    monkeypatch.setattr(
        api_module,
        "DATABASE_PATH",
        test_database,
    )

    return test_database

def test_get_existing_student(
    student_api_database: Path,
) -> None:
    """An existing student should be returned."""

    response = client.get("/students/s002")

    assert response.status_code == 200
    assert response.json() == {
        "student_id": "S002",
        "first_name": "Daniel",
        "last_name": "Degenhardt",
    }
def test_get_unknown_student(
    student_api_database: Path,
) -> None:
    """An unknown student should return HTTP 404."""

    response = client.get("/students/S999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student S999 wurde nicht gefunden.",
    }

@pytest.fixture
def course_api_database(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """Create a temporary course database for API tests."""

    test_database = tmp_path / "course_api.db"

    with sqlite3.connect(test_database) as connection:
        connection.execute(
            """
            CREATE TABLE courses (
                course_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                max_grade REAL NOT NULL,
                passing_grade REAL NOT NULL
            )
            """
        )

        connection.executemany(
            """
            INSERT INTO courses (
                course_id,
                name,
                max_grade,
                passing_grade
            )
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    "AI101",
                    "Artificial Intelligence Basics",
                    100.0,
                    50.0,
                ),
                (
                    "CS102",
                    "Python Programming",
                    100.0,
                    50.0,
                ),
            ],
        )

    monkeypatch.setattr(
        api_module,
        "DATABASE_PATH",
        test_database,
    )

    return test_database

def test_get_courses(
    course_api_database: Path,
) -> None:
    """The courses endpoint should return SQLite courses."""

    response = client.get("/courses")

    assert response.status_code == 200
    assert response.json() == [
        {
            "course_id": "AI101",
            "name": "Artificial Intelligence Basics",
            "max_grade": 100.0,
            "passing_grade": 50.0,
        },
        {
            "course_id": "CS102",
            "name": "Python Programming",
            "max_grade": 100.0,
            "passing_grade": 50.0,
        },
    ]