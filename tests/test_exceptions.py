"""Tests for custom exceptions in the GradeBook system.

This test file checks whether the application raises the correct
custom exceptions in error situations.

The tests cover:
- duplicate students
- duplicate courses
- unknown student IDs
- unknown course IDs
- missing JSON files
- invalid JSON files
- invalid save paths
- missing CSV files
"""

# ============================================================
# Imports
# ============================================================

import pytest

from notenverwaltung.course import Course
from notenverwaltung.exceptions import (
    CourseNotFoundError,
    DuplicateEntryError,
    PersistenceError,
    StudentNotFoundError,
)
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.student import Student


# ============================================================
# Test: Duplicate Student Handling
# ============================================================

def test_duplicate_student_raises_duplicate_entry_error():
    """Test that adding the same student twice raises DuplicateEntryError.

    The GradeBook should not allow two students with the same student ID.
    This test first adds one student and then tries to add the same student
    again. The second attempt must raise a custom DuplicateEntryError.
    """

    gradebook = GradeBook()
    student = Student("S001", "Anna", "Schmidt", "anna@example.com")

    gradebook.add_student(student)

    with pytest.raises(DuplicateEntryError):
        gradebook.add_student(student)


# ============================================================
# Test: Duplicate Course Handling
# ============================================================

def test_duplicate_course_raises_duplicate_entry_error():
    """Test that adding the same course twice raises DuplicateEntryError.

    The GradeBook should not allow two courses with the same course ID.
    This test first adds one course and then tries to add the same course
    again. The second attempt must raise a custom DuplicateEntryError.
    """

    gradebook = GradeBook()
    course = Course("CS101", "Intro to Computer Science")

    gradebook.add_course(course)

    with pytest.raises(DuplicateEntryError):
        gradebook.add_course(course)


# ============================================================
# Test: Unknown Student Handling
# ============================================================

def test_unknown_student_raises_student_not_found_error():
    """Test that recording a grade for an unknown student raises an error.

    A grade can only be recorded if the student already exists in the
    GradeBook. This test uses a student ID that was not added before.
    Therefore, the method must raise StudentNotFoundError.
    """

    gradebook = GradeBook()
    gradebook.add_course(Course("CS101", "Intro to Computer Science"))

    with pytest.raises(StudentNotFoundError):
        gradebook.record_grade("S999", "CS101", 80.0, "2026-07-07")


# ============================================================
# Test: Unknown Course Handling
# ============================================================

def test_unknown_course_raises_course_not_found_error():
    """Test that recording a grade for an unknown course raises an error.

    A grade can only be recorded if the course already exists in the
    GradeBook. This test uses a course ID that was not added before.
    Therefore, the method must raise CourseNotFoundError.
    """

    gradebook = GradeBook()
    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))

    with pytest.raises(CourseNotFoundError):
        gradebook.record_grade("S001", "CS999", 80.0, "2026-07-07")


# ============================================================
# Test: Missing JSON File Handling
# ============================================================

def test_load_json_missing_file_raises_persistence_error(tmp_path):
    """Test that loading a missing JSON file raises PersistenceError.

    The tmp_path fixture creates a temporary test folder.
    This test creates a path to a JSON file that does not exist.
    Loading this missing file must raise PersistenceError.
    """

    file_path = tmp_path / "missing.json"

    with pytest.raises(PersistenceError):
        GradeBook.load_json(str(file_path))


# ============================================================
# Test: Invalid JSON File Handling
# ============================================================

def test_load_json_invalid_file_raises_persistence_error(tmp_path):
    """Test that invalid JSON content raises PersistenceError.

    This test creates a temporary JSON file with broken content.
    The file exists, but its content is not valid JSON.
    Loading this file must raise PersistenceError.
    """

    file_path = tmp_path / "broken.json"
    file_path.write_text("this is not valid json", encoding="utf-8")

    with pytest.raises(PersistenceError):
        GradeBook.load_json(str(file_path))


# ============================================================
# Test: Invalid JSON Save Path Handling
# ============================================================

def test_save_json_to_folder_raises_persistence_error(tmp_path):
    """Test that saving JSON to a folder path raises PersistenceError.

    The save_json method expects a file path, not a folder path.
    This test creates a folder and then tries to save JSON data directly
    into that folder path. This must raise PersistenceError.
    """

    gradebook = GradeBook()
    folder_path = tmp_path / "folder"
    folder_path.mkdir()

    with pytest.raises(PersistenceError):
        gradebook.save_json(str(folder_path))


# ============================================================
# Test: Missing CSV File Handling
# ============================================================

def test_import_csv_missing_file_raises_persistence_error(tmp_path):
    """Test that importing a missing CSV file raises PersistenceError.

    The import method expects an existing CSV file.
    This test creates a path to a CSV file that does not exist.
    Importing this missing file must raise PersistenceError.
    """

    gradebook = GradeBook()
    file_path = tmp_path / "missing.csv"

    with pytest.raises(PersistenceError):
        gradebook.import_grades_from_csv(str(file_path))