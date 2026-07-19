"""Integration tests for the complete Phase 4 database workflow.

These tests connect GradeBook, GradeStore, GradeDatabase, and the domain
classes. They verify dependency injection, SQL statistics, and persistence
in a real temporary SQLite file.
"""

# ============================================================
# Imports
# ============================================================

import pytest

from notenverwaltung.course import Course
from notenverwaltung.database import GradeDatabase
from notenverwaltung.grade_store import InMemoryGradeStore, SqliteGradeStore
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.student import Student


# ============================================================
# Test: Default Dependency
# ============================================================

def test_gradebook_uses_in_memory_store_by_default():
    """Test that old GradeBook() calls keep their original behavior."""

    gradebook = GradeBook()

    assert isinstance(gradebook.store, InMemoryGradeStore)


# ============================================================
# Test: Complete SQLite Workflow
# ============================================================

def test_gradebook_works_with_sqlite_store():
    """Test the full flow from student creation to statistics."""

    database = GradeDatabase(":memory:")
    gradebook = GradeBook(SqliteGradeStore(database))

    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))
    gradebook.add_student(Student("S002", "Ben", "Mueller", "ben@example.com"))

    gradebook.add_course(Course("CS101", "Intro to Computer Science"))
    gradebook.add_course(Course("CS102", "Data Structures"))

    gradebook.record_grade("S001", "CS101", 85.0, "2026-07-07")
    gradebook.record_grade("S001", "CS102", 95.0, "2026-07-08")
    gradebook.record_grade("S002", "CS101", 45.0, "2026-07-07")

    assert len(gradebook.students) == 2
    assert len(gradebook.courses) == 2
    assert len(gradebook.grades) == 3
    assert gradebook.student_average("S001") == pytest.approx(90.0)
    assert gradebook.course_pass_rate("CS101") == pytest.approx(50.0)

    database.close()


# ============================================================
# Test: Python Statistics Compared with SQL Statistics
# ============================================================

def test_python_and_sql_statistics_return_same_results():
    """Compare GradeBook calculations with database aggregation queries."""

    database = GradeDatabase(":memory:")
    gradebook = GradeBook(SqliteGradeStore(database))

    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))
    gradebook.add_student(Student("S002", "Ben", "Mueller", "ben@example.com"))
    gradebook.add_course(Course("CS101", "Intro to Computer Science"))

    gradebook.record_grade("S001", "CS101", 85.0, "2026-07-07")
    gradebook.record_grade("S001", "CS101", 95.0, "2026-07-08")
    gradebook.record_grade("S002", "CS101", 45.0, "2026-07-07")

    assert gradebook.student_average("S001") == pytest.approx(
        database.student_average("S001")
    )
    assert gradebook.course_average("CS101") == pytest.approx(
        database.course_average("CS101")
    )
    assert gradebook.course_pass_rate("CS101") == pytest.approx(
        database.course_pass_rate("CS101")
    )

    database.close()


# ============================================================
# Test: Real SQLite File Persistence
# ============================================================

def test_sqlite_data_remains_after_database_is_reopened(tmp_path):
    """Test that a real SQLite file keeps data between connections."""

    database_path = tmp_path / "grades.db"

    first_database = GradeDatabase(database_path)
    first_gradebook = GradeBook(SqliteGradeStore(first_database))

    first_gradebook.add_student(
        Student("S001", "Anna", "Schmidt", "anna@example.com")
    )
    first_gradebook.add_course(Course("CS101", "Intro to Computer Science"))
    first_gradebook.record_grade("S001", "CS101", 85.0, "2026-07-07")

    first_database.close()

    second_database = GradeDatabase(database_path)
    second_gradebook = GradeBook(SqliteGradeStore(second_database))

    assert second_gradebook.students["S001"].full_name == "Anna Schmidt"
    assert second_gradebook.courses["CS101"].name == "Intro to Computer Science"
    assert len(second_gradebook.grades) == 1
    assert second_gradebook.student_average("S001") == pytest.approx(85.0)

    second_database.close()


# ============================================================
# Test: Existing JSON Conversion with SQLite
# ============================================================

def test_sqlite_gradebook_can_still_be_converted_to_dictionary():
    """Test that Phase 3 JSON preparation also works with SQLite."""

    database = GradeDatabase(":memory:")
    gradebook = GradeBook(SqliteGradeStore(database))

    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))
    gradebook.add_course(Course("CS101", "Intro to Computer Science"))
    gradebook.record_grade(
        "S001",
        "CS101",
        85.0,
        "2026-07-07",
        notes="Database test",
    )

    data = gradebook.to_dict()

    assert data["students"][0]["student_id"] == "S001"
    assert data["courses"][0]["course_id"] == "CS101"
    assert data["grades"][0]["notes"] == "Database test"

    database.close()
