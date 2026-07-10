"""Tests for the Course class.

This test file checks whether Course objects are created correctly
and whether invalid course data raises ValueError.

The tests cover:
- course creation with default values
- course creation with custom values
- empty course IDs
- empty course names
- invalid maximum grades
- invalid passing grades
- readable string output
"""

# ============================================================
# Imports
# ============================================================

import pytest

from notenverwaltung.course import Course


# ============================================================
# Test: Course Creation with Default Values
# ============================================================

def test_course_creation_with_default_values():
    """Test that a course can be created with default grade values.

    This test creates a Course object with only a course ID and a name.
    The max_grade and passing_grade should automatically use their
    default values.

    Expected default values:
    - max_grade: 100.0
    - passing_grade: 50.0
    """

    course = Course(
        course_id="CS101",
        name="Intro to Computer Science",
    )

    assert course.course_id == "CS101"
    assert course.name == "Intro to Computer Science"
    assert course.max_grade == 100.0
    assert course.passing_grade == 50.0


# ============================================================
# Test: Course Creation with Custom Values
# ============================================================

def test_course_creation_with_custom_values():
    """Test that custom max_grade and passing_grade are stored correctly.

    This test creates a Course object with custom grade values.
    It checks whether the given values are saved correctly in the object.
    """

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


# ============================================================
# Test: Empty Course ID Validation
# ============================================================

def test_empty_course_id_raises_value_error():
    """Test that an empty course ID raises ValueError.

    A course must always have a course ID.
    This test checks that an empty course ID is rejected during
    object creation.
    """

    with pytest.raises(ValueError):
        Course("", "Intro to Computer Science")


# ============================================================
# Test: Empty Course Name Validation
# ============================================================

def test_empty_course_name_raises_value_error():
    """Test that an empty course name raises ValueError.

    A course must always have a readable name.
    This test checks that an empty course name is rejected during
    object creation.
    """

    with pytest.raises(ValueError):
        Course("CS101", "")


# ============================================================
# Test: Invalid Maximum Grade Validation
# ============================================================

def test_invalid_max_grade_raises_value_error():
    """Test that max_grade must be greater than zero.

    The maximum grade defines the highest possible score in a course.
    It must be greater than zero because a course cannot have zero
    or negative maximum points.
    """

    with pytest.raises(ValueError):
        Course("CS101", "Intro to Computer Science", max_grade=0)

    with pytest.raises(ValueError):
        Course("CS101", "Intro to Computer Science", max_grade=-10)


# ============================================================
# Test: Invalid Passing Grade Validation
# ============================================================

def test_invalid_passing_grade_raises_value_error():
    """Test that passing_grade must be valid.

    The passing grade must be greater than zero.
    It also must not be greater than the maximum grade.

    This test checks three invalid cases:
    - passing_grade is zero
    - passing_grade is negative
    - passing_grade is higher than max_grade
    """

    with pytest.raises(ValueError):
        Course("CS101", "Intro to Computer Science", passing_grade=0)

    with pytest.raises(ValueError):
        Course("CS101", "Intro to Computer Science", passing_grade=-5)

    with pytest.raises(ValueError):
        Course(
            "CS101",
            "Intro to Computer Science",
            max_grade=100,
            passing_grade=101,
        )


# ============================================================
# Test: Readable String Representation
# ============================================================

def test_readable_string_representation():
    """Test the readable __str__ output of a Course object.

    This test checks whether the Course object returns the expected
    readable text when str(course) is called.
    """

    course = Course("CS101", "Intro to Computer Science")

    assert (
        str(course)
        == "Course: Intro to Computer Science (CS101) | Pass/Max: 50.0/100.0"
    )