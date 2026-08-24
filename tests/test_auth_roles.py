"""Tests für die Rollenverwaltung."""

import sqlite3
from pathlib import Path

import pytest

from notenverwaltung.auth import change_user_role


@pytest.fixture
def role_database(tmp_path: Path) -> Path:
    """Erzeuge für jeden Test eine separate temporäre Datenbank."""

    database_path = tmp_path / "test_roles.db"

    with sqlite3.connect(database_path) as connection:
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
            CREATE TABLE student_accounts (
                student_id TEXT PRIMARY KEY,
                password_salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'student',
                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
            )
            """
        )

        students = [
            ("S001", "Super", "Admin", "super@example.com"),
            ("S002", "Test", "Student", "student@example.com"),
            ("S003", "Test", "Admin", "admin@example.com"),
            ("S004", "Test", "Teacher", "teacher@example.com"),
            ("S005", "Weiterer", "Student", "student2@example.com"),
        ]

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
            students,
        )

        accounts = [
            ("S001", "super_admin"),
            ("S002", "student"),
            ("S003", "admin"),
            ("S004", "teacher"),
            ("S005", "student"),
        ]

        connection.executemany(
            """
            INSERT INTO student_accounts (
                student_id,
                password_salt,
                password_hash,
                role
            )
            VALUES (?, 'test-salt', 'test-hash', ?)
            """,
            accounts,
        )

    return database_path


def test_super_admin_can_change_role(
    role_database: Path,
) -> None:
    """Der Super-Admin darf einen Studenten zum Teacher machen."""

    returned_role, message = change_user_role(
        role_database,
        "S001",
        "super_admin",
        "S002",
        "teacher",
    )

    assert returned_role == "teacher"
    assert "erfolgreich geändert" in message

    with sqlite3.connect(role_database) as connection:
        stored_role = connection.execute(
            """
            SELECT role
            FROM student_accounts
            WHERE student_id = ?
            """,
            ("S002",),
        ).fetchone()[0]

    assert stored_role == "teacher"

@pytest.mark.parametrize(
    (
        "acting_student_id",
        "acting_role",
    ),
    [
        ("S003", "admin"),
        ("S004", "teacher"),
        ("S005", "student"),
    ],
)
def test_non_super_admin_cannot_change_roles(
    role_database: Path,
    acting_student_id: str,
    acting_role: str,
) -> None:
    """Admin, Teacher und Student dürfen keine Rollen ändern."""

    returned_role, message = change_user_role(
        role_database,
        acting_student_id,
        acting_role,
        "S002",
        "admin",
    )

    assert returned_role == ""
    assert "Keine Berechtigung" in message

    with sqlite3.connect(role_database) as connection:
        stored_role = connection.execute(
            """
            SELECT role
            FROM student_accounts
            WHERE student_id = ?
            """,
            ("S002",),
        ).fetchone()[0]

    assert stored_role == "student"

def test_super_admin_role_cannot_be_assigned(
    role_database: Path,
) -> None:
    """Die Rolle super_admin darf nicht neu vergeben werden."""

    returned_role, message = change_user_role(
        role_database,
        "S001",
        "super_admin",
        "S002",
        "super_admin",
    )

    assert returned_role == ""
    assert "Ungültige Rolle" in message

    with sqlite3.connect(role_database) as connection:
        stored_role = connection.execute(
            """
            SELECT role
            FROM student_accounts
            WHERE student_id = ?
            """,
            ("S002",),
        ).fetchone()[0]

    assert stored_role == "student"


def test_existing_super_admin_cannot_be_downgraded(
    role_database: Path,
) -> None:
    """Der vorhandene Super-Admin darf nicht herabgestuft werden."""

    returned_role, message = change_user_role(
        role_database,
        "S001",
        "super_admin",
        "S001",
        "admin",
    )

    assert returned_role == "super_admin"
    assert "nicht verändert" in message

    with sqlite3.connect(role_database) as connection:
        stored_role = connection.execute(
            """
            SELECT role
            FROM student_accounts
            WHERE student_id = ?
            """,
            ("S001",),
        ).fetchone()[0]

    assert stored_role == "super_admin"


def test_invalid_role_is_rejected(
    role_database: Path,
) -> None:
    """Eine unbekannte Fantasierolle muss abgelehnt werden."""

    returned_role, message = change_user_role(
        role_database,
        "S001",
        "super_admin",
        "S002",
        "manager",
    )

    assert returned_role == ""
    assert "Ungültige Rolle" in message

    with sqlite3.connect(role_database) as connection:
        stored_role = connection.execute(
            """
            SELECT role
            FROM student_accounts
            WHERE student_id = ?
            """,
            ("S002",),
        ).fetchone()[0]

    assert stored_role == "student"