import pytest

from notenverwaltung.course import Course
from notenverwaltung.grade import Grade
from notenverwaltung.student import Student


@pytest.fixture
def sample_student():
    """Creates a reusable student for grade tests."""

    return Student(
        student_id="S123",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
    )


@pytest.fixture
def default_course():
    """Creates a reusable course with default grade values."""

    return Course(
        course_id="CS101",
        name="Intro to Computer Science",
        max_grade=100.0,
        passing_grade=50.0,
    )


@pytest.fixture
def custom_course():
    """Creates a reusable course with custom grade values."""

    return Course(
        course_id="MATH201",
        name="Calculus",
        max_grade=6.0,
        passing_grade=4.0,
    )


def test_valid_grade_creation(sample_student, default_course):
    """Tests that a valid grade can be created."""

    grade = Grade(
        student=sample_student,
        course=default_course,
        score=85.0,
        date="2026-07-07",
    )

    assert grade.student == sample_student
    assert grade.course == default_course
    assert grade.score == 85.0
    assert grade.date == "2026-07-07"
    assert grade.notes == ""


def test_score_below_zero_raises_value_error(sample_student, default_course):
    """Tests that a negative score is not allowed."""

    with pytest.raises(ValueError):
        Grade(
            student=sample_student,
            course=default_course,
            score=-1.0,
            date="2026-07-07",
        )


def test_score_above_max_grade_raises_value_error(sample_student, default_course):
    """Tests that a score above max_grade is not allowed."""

    with pytest.raises(ValueError):
        Grade(
            student=sample_student,
            course=default_course,
            score=101.0,
            date="2026-07-07",
        )


def test_invalid_date_format_raises_value_error(sample_student, default_course):
    """Tests that the date must be written in ISO format."""

    with pytest.raises(ValueError):
        Grade(
            student=sample_student,
            course=default_course,
            score=80.0,
            date="07-07-2026",
        )


def test_grade_properties_with_default_course(sample_student, default_course):
    """Tests is_passing, percentage and letter_grade with default values."""

    grade = Grade(
        student=sample_student,
        course=default_course,
        score=92.5,
        date="2026-07-07",
    )

    assert grade.is_passing is True
    assert grade.percentage == 92.5
    assert grade.letter_grade == "A"


def test_failing_grade_with_default_course(sample_student, default_course):
    """Tests a failing grade."""

    grade = Grade(
        student=sample_student,
        course=default_course,
        score=49.9,
        date="2026-07-07",
    )

    assert grade.is_passing is False
    assert grade.letter_grade == "F"


def test_grade_properties_with_custom_course(sample_student, custom_course):
    """Tests grade calculations with a custom max_grade."""

    grade = Grade(
        student=sample_student,
        course=custom_course,
        score=4.5,
        date="2026-07-07",
    )

    assert grade.is_passing is True
    assert grade.percentage == 75.0
    assert grade.letter_grade == "C"


def test_readable_string_representation(sample_student, default_course):
    """Tests the readable __str__ output."""

    grade = Grade(
        student=sample_student,
        course=default_course,
        score=85.0,
        date="2026-07-07",
    )

    expected = "Grade: Jane Doe | Intro to Computer Science | Score: 85.0/100.0 (B) | PASSED"

    assert str(grade) == expected