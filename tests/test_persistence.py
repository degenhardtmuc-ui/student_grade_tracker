"""Tests for JSON persistence and CSV import/export in the GradeBook system.

This test file checks whether a GradeBook object can be converted into
dictionary data, saved as JSON, loaded from JSON, exported to CSV,
and filled again by importing grades from a CSV file.
"""

import json

from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.student import Student


# ============================================================
# Helper Function: Create Sample GradeBook Data
# ============================================================

def create_sample_gradebook() -> GradeBook:
    """Create a small reusable GradeBook object for persistence tests.

    The sample GradeBook contains two students, two courses, and three grades.
    This helper function avoids repeated setup code in the test functions.
    """

    gradebook = GradeBook()

    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))
    gradebook.add_student(Student("S002", "Ben", "Mueller", "ben@example.com"))

    gradebook.add_course(Course("CS101", "Intro to Computer Science"))
    gradebook.add_course(Course("CS102", "Data Structures"))

    gradebook.record_grade("S001", "CS101", 85.0, "2026-07-07")
    gradebook.record_grade("S001", "CS102", 95.0, "2026-07-08")
    gradebook.record_grade("S002", "CS101", 45.0, "2026-07-07")

    return gradebook


# ============================================================
# Test: Convert GradeBook to Dictionary
# ============================================================

def test_to_dict_contains_students_courses_and_grades():
    """Test that a GradeBook is converted into dictionary data.

    The dictionary must contain the main keys for students, courses,
    and grades. The test also checks whether the correct number of
    entries is stored in each section.
    """

    gradebook = create_sample_gradebook()

    data = gradebook.to_dict()

    assert "students" in data
    assert "courses" in data
    assert "grades" in data

    assert len(data["students"]) == 2
    assert len(data["courses"]) == 2
    assert len(data["grades"]) == 3


# ============================================================
# Test: Rebuild GradeBook from Dictionary
# ============================================================

def test_from_dict_creates_gradebook_again():
    """Test that a GradeBook can be rebuilt from dictionary data.

    This test first converts a GradeBook into a dictionary and then
    creates a new GradeBook from this dictionary. The loaded GradeBook
    should contain the same amount of students, courses, and grades.
    """

    original_gradebook = create_sample_gradebook()

    data = original_gradebook.to_dict()
    loaded_gradebook = GradeBook.from_dict(data)

    assert len(loaded_gradebook.students) == 2
    assert len(loaded_gradebook.courses) == 2
    assert len(loaded_gradebook.grades) == 3

    assert loaded_gradebook.student_average("S001") == 90.0


# ============================================================
# Test: Save GradeBook as JSON File
# ============================================================

def test_save_json_creates_json_file(tmp_path):
    """Test that a GradeBook can be saved as a JSON file.

    The tmp_path fixture creates a temporary folder for the test.
    This makes sure that the test does not create real files inside
    the project folder.
    """

    gradebook = create_sample_gradebook()
    file_path = tmp_path / "gradebook.json"

    gradebook.save_json(str(file_path))

    assert file_path.exists()

    json_text = file_path.read_text(encoding="utf-8")
    data = json.loads(json_text)

    assert "students" in data
    assert "courses" in data
    assert "grades" in data


# ============================================================
# Test: Load GradeBook from JSON File
# ============================================================

def test_load_json_loads_gradebook_from_file(tmp_path):
    """Test that a GradeBook can be loaded from a JSON file.

    This test saves a GradeBook as JSON first and then loads it again.
    After loading, the new GradeBook should contain the same data as before.
    """

    original_gradebook = create_sample_gradebook()
    file_path = tmp_path / "gradebook.json"

    original_gradebook.save_json(str(file_path))

    loaded_gradebook = GradeBook.load_json(str(file_path))

    assert len(loaded_gradebook.students) == 2
    assert len(loaded_gradebook.courses) == 2
    assert len(loaded_gradebook.grades) == 3

    assert loaded_gradebook.course_pass_rate("CS101") == 50.0


# ============================================================
# Test: Export Grades to CSV File
# ============================================================

def test_export_grades_to_csv_creates_csv_file(tmp_path):
    """Test that all grades are exported into a CSV file.

    The exported CSV file should contain a header row and the expected
    grade rows for the stored students and courses.
    """

    gradebook = create_sample_gradebook()
    file_path = tmp_path / "grades.csv"

    gradebook.export_grades_to_csv(str(file_path))

    assert file_path.exists()

    csv_text = file_path.read_text(encoding="utf-8")

    assert "student_id,course_id,score,date" in csv_text
    assert "S001,CS101,85.0,2026-07-07" in csv_text
    assert "S002,CS101,45.0,2026-07-07" in csv_text


# ============================================================
# Test: Import Valid Grades from CSV File
# ============================================================

def test_import_grades_from_csv_imports_valid_lines(tmp_path):
    """Test that valid CSV lines are imported as grades.

    This test creates a temporary CSV file with valid grade data.
    After importing the file, the GradeBook should contain the imported grades.
    The import report should show that no lines were skipped.
    """

    gradebook = GradeBook()

    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))
    gradebook.add_student(Student("S002", "Ben", "Mueller", "ben@example.com"))

    gradebook.add_course(Course("CS101", "Intro to Computer Science"))

    file_path = tmp_path / "grades.csv"

    file_path.write_text(
        "student_id,course_id,score,date\n"
        "S001,CS101,85.0,2026-07-07\n"
        "S002,CS101,45.0,2026-07-07",
        encoding="utf-8",
    )

    report = gradebook.import_grades_from_csv(str(file_path))

    assert report["imported"] == 2
    assert report["skipped"] == 0
    assert len(report["errors"]) == 0
    assert len(gradebook.grades) == 2


# ============================================================
# Test: Skip Invalid CSV Lines
# ============================================================

def test_import_grades_from_csv_skips_invalid_lines(tmp_path):
    """Test that invalid CSV lines are skipped and reported.

    This test imports a CSV file that contains one valid line and two
    invalid lines. The GradeBook should only store the valid grade.
    The import report should count the skipped lines and store error messages.
    """

    gradebook = GradeBook()

    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))
    gradebook.add_course(Course("CS101", "Intro to Computer Science"))

    file_path = tmp_path / "grades.csv"

    file_path.write_text(
        "student_id,course_id,score,date\n"
        "S001,CS101,85.0,2026-07-07\n"
        "this,is,not,valid,enough\n"
        "S999,CS101,70.0,2026-07-07",
        encoding="utf-8",
    )

    report = gradebook.import_grades_from_csv(str(file_path))

    assert report["imported"] == 1
    assert report["skipped"] == 2
    assert len(report["errors"]) == 2
    assert len(gradebook.grades) == 1