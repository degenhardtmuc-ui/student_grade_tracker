import json

from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.student import Student


def create_sample_gradebook() -> GradeBook:
    """Creates a small reusable grade book for persistence tests."""
    gradebook = GradeBook()

    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))
    gradebook.add_student(Student("S002", "Ben", "Mueller", "ben@example.com"))

    gradebook.add_course(Course("CS101", "Intro to Computer Science"))
    gradebook.add_course(Course("CS102", "Data Structures"))

    gradebook.record_grade("S001", "CS101", 85.0, "2026-07-07")
    gradebook.record_grade("S001", "CS102", 95.0, "2026-07-08")
    gradebook.record_grade("S002", "CS101", 45.0, "2026-07-07")

    return gradebook


def test_to_dict_contains_students_courses_and_grades():
    """Tests that GradeBook is converted into dictionary data."""
    gradebook = create_sample_gradebook()

    data = gradebook.to_dict()

    assert "students" in data
    assert "courses" in data
    assert "grades" in data

    assert len(data["students"]) == 2
    assert len(data["courses"]) == 2
    assert len(data["grades"]) == 3


def test_from_dict_creates_gradebook_again():
    """Tests that a GradeBook can be rebuilt from dictionary data."""
    original_gradebook = create_sample_gradebook()

    data = original_gradebook.to_dict()
    loaded_gradebook = GradeBook.from_dict(data)

    assert len(loaded_gradebook.students) == 2
    assert len(loaded_gradebook.courses) == 2
    assert len(loaded_gradebook.grades) == 3

    assert loaded_gradebook.student_average("S001") == 90.0


def test_save_json_creates_json_file(tmp_path):
    """Tests that a JSON file is created."""
    gradebook = create_sample_gradebook()
    file_path = tmp_path / "gradebook.json"

    gradebook.save_json(str(file_path))

    assert file_path.exists()

    json_text = file_path.read_text(encoding="utf-8")
    data = json.loads(json_text)

    assert "students" in data
    assert "courses" in data
    assert "grades" in data


def test_load_json_loads_gradebook_from_file(tmp_path):
    """Tests that a GradeBook can be loaded from a JSON file."""
    original_gradebook = create_sample_gradebook()
    file_path = tmp_path / "gradebook.json"

    original_gradebook.save_json(str(file_path))

    loaded_gradebook = GradeBook.load_json(str(file_path))

    assert len(loaded_gradebook.students) == 2
    assert len(loaded_gradebook.courses) == 2
    assert len(loaded_gradebook.grades) == 3

    assert loaded_gradebook.course_pass_rate("CS101") == 50.0


def test_export_grades_to_csv_creates_csv_file(tmp_path):
    """Tests that grades are exported as a CSV file."""
    gradebook = create_sample_gradebook()
    file_path = tmp_path / "grades.csv"

    gradebook.export_grades_to_csv(str(file_path))

    assert file_path.exists()

    csv_text = file_path.read_text(encoding="utf-8")

    assert "student_id,course_id,score,date" in csv_text
    assert "S001,CS101,85.0,2026-07-07" in csv_text
    assert "S002,CS101,45.0,2026-07-07" in csv_text


def test_import_grades_from_csv_imports_valid_lines(tmp_path):
    """Tests that valid CSV lines are imported as grades."""
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


def test_import_grades_from_csv_skips_invalid_lines(tmp_path):
    """Tests that invalid CSV lines are skipped and reported."""
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