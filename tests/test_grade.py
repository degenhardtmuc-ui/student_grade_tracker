"""Tests for the Grade class.

This test file checks whether Grade objects are created correctly
and whether invalid grade data raises ValueError.

The tests cover:
- reusable pytest fixtures
- valid grade creation
- invalid negative scores
- scores above the maximum grade
- invalid date formats
- passing and failing grades
- percentage calculation
- letter grade calculation
- readable string output
"""

# ============================================================
# Imports
# ============================================================

import pytest

from notenverwaltung.course import Course
from notenverwaltung.grade import Grade
from notenverwaltung.student import Student


# ============================================================
# Fixture: Reusable Student for Grade Tests
# ============================================================

@pytest.fixture
def sample_student():
    """Create a reusable Student object for grade tests.

    This fixture avoids repeated student setup code in the test functions.
    Pytest automatically provides this student to every test function
    that uses the sample_student parameter.
    """

    return Student(
        student_id="S123",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
    )


# ============================================================
# Fixture: Reusable Course with Default Grade Values
# ============================================================

@pytest.fixture
def default_course():
    """Create a reusable Course object with default grade values.

    This fixture creates a course with:
    - max_grade: 100.0
    - passing_grade: 50.0

    It is used to test normal percentage-based grade behavior.
    """

    return Course(
        course_id="CS101",
        name="Intro to Computer Science",
        max_grade=100.0,
        passing_grade=50.0,
    )


# ============================================================
# Fixture: Reusable Course with Custom Grade Values
# ============================================================

@pytest.fixture
def custom_course():
    """Create a reusable Course object with custom grade values.

    This fixture creates a course with a different grading scale.
    It is used to test whether Grade calculations also work when
    max_grade and passing_grade are not based on 100 points.
    """

    return Course(
        course_id="MATH201",
        name="Calculus",
        max_grade=6.0,
        passing_grade=4.0,
    )


# ============================================================
# Test: Valid Grade Creation
# ============================================================

def test_valid_grade_creation(sample_student, default_course):
    """Test that a valid Grade object can be created.

    This test checks whether the student, course, score, date,
    and default notes value are stored correctly.
    """

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


# ============================================================
# Test: Score Below Zero Validation
# ============================================================

def test_score_below_zero_raises_value_error(sample_student, default_course):
    """Test that a negative score raises ValueError.

    A score must not be below zero.
    This test checks whether the Grade class rejects negative scores
    during object creation.
    """

    with pytest.raises(ValueError):
        Grade(
            student=sample_student,
            course=default_course,
            score=-1.0,
            date="2026-07-07",
        )


# ============================================================
# Test: Score Above Maximum Grade Validation
# ============================================================

def test_score_above_max_grade_raises_value_error(sample_student, default_course):
    """Test that a score above max_grade raises ValueError.

    A score must not be higher than the maximum grade of the course.
    This test checks whether the Grade class rejects scores that are
    too high.
    """

    with pytest.raises(ValueError):
        Grade(
            student=sample_student,
            course=default_course,
            score=101.0,
            date="2026-07-07",
        )


# ============================================================
# Test: Invalid Date Format Validation
# ============================================================

def test_invalid_date_format_raises_value_error(sample_student, default_course):
    """Test that an invalid date format raises ValueError.

    The Grade class expects the date in ISO format.

    Example of a valid ISO date:
    2026-07-07

    This test uses an invalid date format and expects ValueError.
    """

    with pytest.raises(ValueError):
        Grade(
            student=sample_student,
            course=default_course,
            score=80.0,
            date="07-07-2026",
        )


# ============================================================
# Test: Grade Properties with Default Course
# ============================================================

def test_grade_properties_with_default_course(sample_student, default_course):
    """Test is_passing, percentage, and letter_grade with default values.

    This test uses a normal course with 100 maximum points.
    A score of 92.5 should:
    - pass the course
    - return 92.5 percent
    - result in letter grade A
    """

    grade = Grade(
        student=sample_student,
        course=default_course,
        score=92.5,
        date="2026-07-07",
    )

    assert grade.is_passing is True
    assert grade.percentage == 92.5
    assert grade.letter_grade == "A"


# ============================================================
# Test: Failing Grade with Default Course
# ============================================================

def test_failing_grade_with_default_course(sample_student, default_course):
    """Test a failing grade with the default course values.

    This test uses a score below the passing grade.
    The grade should not be passing and should result in letter grade F.
    """

    grade = Grade(
        student=sample_student,
        course=default_course,
        score=49.9,
        date="2026-07-07",
    )

    assert grade.is_passing is False
    assert grade.letter_grade == "F"


# ============================================================
# Test: Grade Properties with Custom Course
# ============================================================

def test_grade_properties_with_custom_course(sample_student, custom_course):
    """Test grade calculations with a custom maximum grade.

    This test uses a course with max_grade 6.0 and passing_grade 4.0.
    A score of 4.5 should:
    - pass the course
    - return 75.0 percent
    - result in letter grade C
    """

    grade = Grade(
        student=sample_student,
        course=custom_course,
        score=4.5,
        date="2026-07-07",
    )

    assert grade.is_passing is True
    assert grade.percentage == 75.0
    assert grade.letter_grade == "C"


# ============================================================
# Test: Readable String Representation
# ============================================================

def test_readable_string_representation(sample_student, default_course):
    """Test the readable __str__ output of a Grade object.

    This test checks whether str(grade) returns the expected text.
    The output should contain:
    - the student's full name
    - the course name
    - the score and maximum grade
    - the letter grade
    - the passing status
    """

    grade = Grade(
        student=sample_student,
        course=default_course,
        score=85.0,
        date="2026-07-07",
    )

    expected = (
        "Grade: Jane Doe | Intro to Computer Science | "
        "Score: 85.0/100.0 (B) | PASSED"
    )

    assert str(grade) == expected