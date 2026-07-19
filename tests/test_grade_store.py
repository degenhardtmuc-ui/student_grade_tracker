"""Contract tests for both GradeStore implementations.

The same tests run once with InMemoryGradeStore and once with
SqliteGradeStore. This verifies that both classes fulfill the same
abstract interface and show the same basic behavior.
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
    StudentNotFoundError,
)
from notenverwaltung.grade import Grade
from notenverwaltung.grade_store import (
    GradeStore,
    InMemoryGradeStore,
    SqliteGradeStore,
)
from notenverwaltung.student import Student


# ============================================================
# Fixture: Run Tests with Both Storage Implementations
# ============================================================

@pytest.fixture(params=["memory", "sqlite"])
def store(request):
    """Provide an in-memory store and a SQLite store one after another."""

    if request.param == "memory":
        yield InMemoryGradeStore()
        return

    database = GradeDatabase(":memory:")
    yield SqliteGradeStore(database)
    database.close()


# ============================================================
# Test: Abstract Interface
# ============================================================

def test_store_is_grade_store(store):
    """Test that both implementations inherit from GradeStore."""

    assert isinstance(store, GradeStore)


# ============================================================
# Test: Student Storage Contract
# ============================================================

def test_store_adds_and_gets_student(store):
    """Test the common student storage behavior."""

    student = Student("S001", "Anna", "Schmidt", "anna@example.com")

    store.add_student(student)

    assert store.get_student("S001") == student
    assert store.get_all_students() == [student]


# ============================================================
# Test: Duplicate Student Contract
# ============================================================

def test_store_rejects_duplicate_student(store):
    """Test that both stores use DuplicateEntryError."""

    student = Student("S001", "Anna", "Schmidt", "anna@example.com")
    store.add_student(student)

    with pytest.raises(DuplicateEntryError):
        store.add_student(student)


# ============================================================
# Test: Course Storage Contract
# ============================================================

def test_store_adds_and_gets_course(store):
    """Test the common course storage behavior."""

    course = Course("CS101", "Intro to Computer Science")

    store.add_course(course)

    assert store.get_course("CS101") == course
    assert store.get_all_courses() == [course]


# ============================================================
# Test: Duplicate Course Contract
# ============================================================

def test_store_rejects_duplicate_course(store):
    """Test that both stores reject duplicate course IDs."""

    course = Course("CS101", "Intro to Computer Science")
    store.add_course(course)

    with pytest.raises(DuplicateEntryError):
        store.add_course(course)


# ============================================================
# Test: Grade Storage Contract
# ============================================================

def test_store_records_and_filters_grades(store):
    """Test the common grade recording and lookup behavior."""

    student = Student("S001", "Anna", "Schmidt", "anna@example.com")
    course = Course("CS101", "Intro to Computer Science")
    grade = Grade(student, course, 85.0, "2026-07-07")

    store.add_student(student)
    store.add_course(course)
    store.record_grade(grade)

    assert store.get_all_grades() == [grade]
    assert store.get_student_grades("S001") == [grade]
    assert store.get_course_grades("CS101") == [grade]


# ============================================================
# Test: Missing Student Contract
# ============================================================

def test_store_raises_error_for_unknown_student(store):
    """Test the common StudentNotFoundError behavior."""

    with pytest.raises(StudentNotFoundError):
        store.get_student("S999")


# ============================================================
# Test: Missing Course Contract
# ============================================================

def test_store_raises_error_for_unknown_course(store):
    """Test the common CourseNotFoundError behavior."""

    with pytest.raises(CourseNotFoundError):
        store.get_course("CS999")


# ============================================================
# Test: Update and Delete Contract
# ============================================================

def test_store_updates_and_deletes_student_and_course(store):
    """Test common update and delete operations without grades."""

    student = Student("S001", "Anna", "Schmidt", "anna@example.com")
    course = Course("CS101", "Intro to Computer Science")

    store.add_student(student)
    store.add_course(course)

    updated_student = Student("S001", "Anna Maria", "Schmidt", "new@example.com")
    updated_course = Course("CS101", "Python Fundamentals")

    store.update_student(updated_student)
    store.update_course(updated_course)

    assert store.get_student("S001") == updated_student
    assert store.get_course("CS101") == updated_course

    store.delete_student("S001")
    store.delete_course("CS101")

    with pytest.raises(StudentNotFoundError):
        store.get_student("S001")

    with pytest.raises(CourseNotFoundError):
        store.get_course("CS101")
