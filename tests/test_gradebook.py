import pytest

from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.student import Student


@pytest.fixture
def sample_gradebook():
    """Creates a reusable grade book for tests."""
    gradebook = GradeBook()

    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))
    gradebook.add_student(Student("S002", "Ben", "Mueller", "ben@example.com"))
    gradebook.add_student(Student("S003", "Clara", "Weber", "clara@example.com"))

    gradebook.add_course(Course("CS101", "Intro to Computer Science"))
    gradebook.add_course(Course("CS102", "Data Structures"))

    gradebook.record_grade("S001", "CS101", 85.0, "2026-07-07")
    gradebook.record_grade("S001", "CS102", 95.0, "2026-07-08")
    gradebook.record_grade("S002", "CS101", 45.0, "2026-07-07")
    gradebook.record_grade("S003", "CS101", 70.0, "2026-07-07")

    return gradebook


def test_add_student():
    """Tests that a student can be added."""
    gradebook = GradeBook()
    student = Student("S001", "Anna", "Schmidt", "anna@example.com")

    gradebook.add_student(student)

    assert gradebook.students["S001"] == student


def test_add_duplicate_student_raises_value_error():
    """Tests that duplicate student IDs are not allowed."""
    gradebook = GradeBook()
    student = Student("S001", "Anna", "Schmidt", "anna@example.com")

    gradebook.add_student(student)

    with pytest.raises(ValueError):
        gradebook.add_student(student)


def test_add_course():
    """Tests that a course can be added."""
    gradebook = GradeBook()
    course = Course("CS101", "Intro to Computer Science")

    gradebook.add_course(course)

    assert gradebook.courses["CS101"] == course


def test_add_duplicate_course_raises_value_error():
    """Tests that duplicate course IDs are not allowed."""
    gradebook = GradeBook()
    course = Course("CS101", "Intro to Computer Science")

    gradebook.add_course(course)

    with pytest.raises(ValueError):
        gradebook.add_course(course)


def test_record_grade(sample_gradebook):
    """Tests that record_grade creates and stores a grade."""
    grade = sample_gradebook.record_grade("S001", "CS101", 90.0, "2026-07-09")

    assert grade.student.student_id == "S001"
    assert grade.course.course_id == "CS101"
    assert grade.score == 90.0
    assert grade in sample_gradebook.grades


def test_record_grade_unknown_student_raises_value_error(sample_gradebook):
    """Tests that a grade cannot be recorded for an unknown student."""
    with pytest.raises(ValueError):
        sample_gradebook.record_grade("S999", "CS101", 80.0, "2026-07-07")


def test_record_grade_unknown_course_raises_value_error(sample_gradebook):
    """Tests that a grade cannot be recorded for an unknown course."""
    with pytest.raises(ValueError):
        sample_gradebook.record_grade("S001", "CS999", 80.0, "2026-07-07")


def test_get_student_grades(sample_gradebook):
    """Tests that only grades for one student are returned."""
    grades = sample_gradebook.get_student_grades("S001")

    assert len(grades) == 2
    assert all(grade.student.student_id == "S001" for grade in grades)


def test_get_course_grades(sample_gradebook):
    """Tests that only grades for one course are returned."""
    grades = sample_gradebook.get_course_grades("CS101")

    assert len(grades) == 3
    assert all(grade.course.course_id == "CS101" for grade in grades)


def test_student_average(sample_gradebook):
    """Tests the average percentage for one student."""
    average = sample_gradebook.student_average("S001")

    assert average == pytest.approx(90.0)


def test_course_average(sample_gradebook):
    """Tests the average score for one course."""
    average = sample_gradebook.course_average("CS101")

    assert average == pytest.approx(66.6666667)


def test_course_pass_rate(sample_gradebook):
    """Tests the percentage of passing grades for one course."""
    pass_rate = sample_gradebook.course_pass_rate("CS101")

    assert pass_rate == pytest.approx(66.6666667)


def test_top_students(sample_gradebook):
    """Tests that the best students are returned first."""
    top_students = sample_gradebook.top_students(n=2)

    assert len(top_students) == 2
    assert top_students[0][0].student_id == "S001"
    assert top_students[0][1] == pytest.approx(90.0)


def test_students_at_risk(sample_gradebook):
    """Tests that students below the threshold are returned."""
    at_risk = sample_gradebook.students_at_risk(threshold=60.0)

    assert len(at_risk) == 1
    assert at_risk[0].student_id == "S002"


def test_search_students_by_name(sample_gradebook):
    """Tests regex search for students by name."""
    result = sample_gradebook.search_students("anna")

    assert len(result) == 1
    assert result[0].student_id == "S001"


def test_search_students_by_email(sample_gradebook):
    """Tests regex search for students by email."""
    result = sample_gradebook.search_students("clara@example")

    assert len(result) == 1
    assert result[0].student_id == "S003"


def test_search_courses(sample_gradebook):
    """Tests regex search for courses by course name."""
    result = sample_gradebook.search_courses("data")

    assert len(result) == 1
    assert result[0].course_id == "CS102"


def test_no_grades_for_student_raises_value_error():
    """Tests that average calculation fails when a student has no grades."""
    gradebook = GradeBook()
    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))

    with pytest.raises(ValueError):
        gradebook.student_average("S001")


def test_no_grades_for_course_raises_value_error():
    """Tests that average calculation fails when a course has no grades."""
    gradebook = GradeBook()
    gradebook.add_course(Course("CS101", "Intro to Computer Science"))

    with pytest.raises(ValueError):
        gradebook.course_average("CS101")


def test_returned_student_grades_do_not_change_internal_list(sample_gradebook):
    """Tests that modifying the returned list does not modify the grade book."""
    grades = sample_gradebook.get_student_grades("S001")
    grades.clear()

    assert len(sample_gradebook.get_student_grades("S001")) == 2
    assert len(sample_gradebook.grades) == 4