"""Tests for the SQLite GradeDatabase class.

These tests use an in-memory SQLite database. The database exists only
during one test and does not create a real database file in the project.

The tests cover:
- the relational database schema
- CRUD operations for students, courses, and grades
- custom exceptions
- SQL aggregation with AVG, COUNT, GROUP BY, and JOIN
"""

# ============================================================
# Imports
# ============================================================

import pytest

from notenverwaltung.course import Course
from notenverwaltung.database import GradeDatabase
from notenverwaltung.exceptions import (
    CourseNotFoundError,
    DuplicateEntryError,
    PersistenceError,
    StudentNotFoundError,
)
from notenverwaltung.grade import Grade
from notenverwaltung.student import Student


# ============================================================
# Fixture: Empty In-Memory SQLite Database
# ============================================================

@pytest.fixture
def database():
    """Create and close a fresh in-memory database for every test."""

    grade_database = GradeDatabase(":memory:")

    yield grade_database

    grade_database.close()


# ============================================================
# Helper Function: Add Reusable Database Data
# ============================================================

def add_sample_data(database: GradeDatabase) -> None:
    """Add three students, two courses, and four grades."""

    student_1 = Student("S001", "Anna", "Schmidt", "anna@example.com")
    student_2 = Student("S002", "Ben", "Mueller", "ben@example.com")
    student_3 = Student("S003", "Clara", "Weber", "clara@example.com")

    course_1 = Course("CS101", "Intro to Computer Science")
    course_2 = Course("CS102", "Data Structures")

    database.add_student(student_1)
    database.add_student(student_2)
    database.add_student(student_3)

    database.add_course(course_1)
    database.add_course(course_2)

    database.record_grade(Grade(student_1, course_1, 85.0, "2026-07-07"))
    database.record_grade(Grade(student_1, course_2, 95.0, "2026-07-08"))
    database.record_grade(Grade(student_2, course_1, 45.0, "2026-07-07"))
    database.record_grade(Grade(student_3, course_1, 70.0, "2026-07-07"))


# ============================================================
# Test: Database Schema
# ============================================================

def test_database_creates_required_tables(database):
    """Test that students, courses, and grades are created."""

    rows = database.connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()

    table_names = {row["name"] for row in rows}

    assert "students" in table_names
    assert "courses" in table_names
    assert "grades" in table_names


# ============================================================
# Test: Student CRUD
# ============================================================

def test_student_create_read_update_and_delete(database):
    """Test all four CRUD operations for one student."""

    student = Student("S001", "Anna", "Schmidt", "anna@example.com")
    database.add_student(student)

    assert database.get_student("S001") == student

    updated_student = Student(
        "S001",
        "Anna Maria",
        "Schmidt",
        "anna.maria@example.com",
    )
    database.update_student(updated_student)

    assert database.get_student("S001") == updated_student

    database.delete_student("S001")

    with pytest.raises(StudentNotFoundError):
        database.get_student("S001")


# ============================================================
# Test: Duplicate Student
# ============================================================

def test_duplicate_student_raises_duplicate_entry_error(database):
    """Test that the student primary key prevents duplicate IDs."""

    student = Student("S001", "Anna", "Schmidt", "anna@example.com")
    database.add_student(student)

    with pytest.raises(DuplicateEntryError):
        database.add_student(student)


# ============================================================
# Test: Course CRUD
# ============================================================

def test_course_create_read_update_and_delete(database):
    """Test all four CRUD operations for one course."""

    course = Course("CS101", "Intro to Computer Science")
    database.add_course(course)

    assert database.get_course("CS101") == course

    updated_course = Course(
        "CS101",
        "Python Fundamentals",
        max_grade=120.0,
        passing_grade=60.0,
    )
    database.update_course(updated_course)

    assert database.get_course("CS101") == updated_course

    database.delete_course("CS101")

    with pytest.raises(CourseNotFoundError):
        database.get_course("CS101")


# ============================================================
# Test: Duplicate Course
# ============================================================

def test_duplicate_course_raises_duplicate_entry_error(database):
    """Test that the course primary key prevents duplicate IDs."""

    course = Course("CS101", "Intro to Computer Science")
    database.add_course(course)

    with pytest.raises(DuplicateEntryError):
        database.add_course(course)


# ============================================================
# Test: Grade CRUD
# ============================================================

def test_grade_create_read_update_and_delete(database):
    """Test all four CRUD operations for one grade."""

    student = Student("S001", "Anna", "Schmidt", "anna@example.com")
    course = Course("CS101", "Intro to Computer Science")

    database.add_student(student)
    database.add_course(course)

    grade = Grade(student, course, 85.0, "2026-07-07", "First attempt")
    grade_id = database.record_grade(grade)

    assert database.get_grade(grade_id) == grade

    updated_grade = Grade(student, course, 92.0, "2026-07-09", "Updated")
    database.update_grade(grade_id, updated_grade)

    assert database.get_grade(grade_id) == updated_grade

    database.delete_grade(grade_id)

    with pytest.raises(ValueError):
        database.get_grade(grade_id)


# ============================================================
# Test: Foreign Key Checks
# ============================================================

def test_grade_requires_existing_student_and_course(database):
    """Test clear custom errors for missing related records."""

    unknown_student = Student("S999", "Unknown", "Person", "unknown@example.com")
    unknown_course = Course("CS999", "Unknown Course")

    with pytest.raises(StudentNotFoundError):
        database.record_grade(
            Grade(unknown_student, unknown_course, 80.0, "2026-07-07")
        )

    database.add_student(unknown_student)

    with pytest.raises(CourseNotFoundError):
        database.record_grade(
            Grade(unknown_student, unknown_course, 80.0, "2026-07-07")
        )


# ============================================================
# Test: Foreign Keys Protect Existing Grades
# ============================================================

def test_student_and_course_with_grades_cannot_be_deleted(database):
    """Test that foreign keys protect referenced students and courses."""

    add_sample_data(database)

    with pytest.raises(PersistenceError):
        database.delete_student("S001")

    with pytest.raises(PersistenceError):
        database.delete_course("CS101")


# ============================================================
# Test: Grade Lookups
# ============================================================

def test_get_grades_by_student_and_course(database):
    """Test database grade filters for student and course IDs."""

    add_sample_data(database)

    student_grades = database.get_student_grades("S001")
    course_grades = database.get_course_grades("CS101")

    assert len(student_grades) == 2
    assert len(course_grades) == 3
    assert all(grade.student.student_id == "S001" for grade in student_grades)
    assert all(grade.course.course_id == "CS101" for grade in course_grades)


# ============================================================
# Test: SQL Average and Pass Rate
# ============================================================

def test_sql_average_and_pass_rate(database):
    """Test statistics calculated directly with SQL AVG and JOIN."""

    add_sample_data(database)

    assert database.student_average("S001") == pytest.approx(90.0)
    assert database.course_average("CS101") == pytest.approx(66.6666667)
    assert database.course_pass_rate("CS101") == pytest.approx(66.6666667)


# ============================================================
# Test: SQL GROUP BY
# ============================================================

def test_sql_student_averages_use_grouping(database):
    """Test the grouped list of student average percentages."""

    add_sample_data(database)

    averages = database.student_averages()

    assert averages[0] == ("S001", pytest.approx(90.0))
    assert averages[1] == ("S003", pytest.approx(70.0))
    assert averages[2] == ("S002", pytest.approx(45.0))


# ============================================================
# Test: SQL COUNT, AVG, GROUP BY, and LEFT JOIN
# ============================================================

def test_sql_course_statistics(database):
    """Test the complete grouped SQL statistics for every course."""

    add_sample_data(database)

    statistics = database.course_statistics()

    cs101 = statistics[0]
    cs102 = statistics[1]

    assert cs101["course_id"] == "CS101"
    assert cs101["grade_count"] == 3
    assert cs101["average_score"] == pytest.approx(66.6666667)
    assert cs101["pass_rate"] == pytest.approx(66.6666667)

    assert cs102["course_id"] == "CS102"
    assert cs102["grade_count"] == 1
    assert cs102["average_score"] == pytest.approx(95.0)
    assert cs102["pass_rate"] == pytest.approx(100.0)
