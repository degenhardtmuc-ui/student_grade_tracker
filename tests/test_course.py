import pytest

from notenverwaltung.course import Course


def test_course_creation_with_default_values():
    """Tests that a course can be created with default grade values."""

    course = Course(
        course_id="CS101",
        name="Intro to Computer Science",
    )

    assert course.course_id == "CS101"
    assert course.name == "Intro to Computer Science"
    assert course.max_grade == 100.0
    assert course.passing_grade == 50.0


def test_course_creation_with_custom_values():
    """Tests that custom max_grade and passing_grade are stored correctly."""

    course = Course(
        course_id="MATH201",
        name="Calculus",
        max_grade=6.0,
        passing_grade=4.0,
    )

    assert course.course_id == "MATH201"
    assert course.name == "Calculus"
    assert course.max_grade == 6.0
    assert course.passing_grade == 4.0


def test_empty_course_id_raises_value_error():
    """Tests that an empty course_id is not allowed."""

    with pytest.raises(ValueError):
        Course("", "Intro to Computer Science")


def test_empty_course_name_raises_value_error():
    """Tests that an empty course name is not allowed."""

    with pytest.raises(ValueError):
        Course("CS101", "")


def test_invalid_max_grade_raises_value_error():
    """Tests that max_grade must be greater than 0."""

    with pytest.raises(ValueError):
        Course("CS101", "Intro to Computer Science", max_grade=0)

    with pytest.raises(ValueError):
        Course("CS101", "Intro to Computer Science", max_grade=-10)


def test_invalid_passing_grade_raises_value_error():
    """Tests that passing_grade must be greater than 0 and not above max_grade."""

    with pytest.raises(ValueError):
        Course("CS101", "Intro to Computer Science", passing_grade=0)

    with pytest.raises(ValueError):
        Course("CS101", "Intro to Computer Science", passing_grade=-5)

    with pytest.raises(ValueError):
        Course("CS101", "Intro to Computer Science", max_grade=100, passing_grade=101)


def test_readable_string_representation():
    """Tests the readable __str__ output."""

    course = Course("CS101", "Intro to Computer Science")

    assert str(course) == "Course: Intro to Computer Science (CS101) | Pass/Max: 50.0/100.0"