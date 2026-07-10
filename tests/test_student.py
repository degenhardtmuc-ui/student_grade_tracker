"""Tests for the Student class.

This test file checks whether Student objects are created correctly
and whether invalid student data raises ValueError.

The tests cover:
- valid student creation
- full name property
- readable string output
- empty student IDs
- empty first names
- empty last names
- invalid email addresses
"""

# ============================================================
# Imports
# ============================================================

import pytest

from notenverwaltung.student import Student


# ============================================================
# Test: Valid Student Creation
# ============================================================

def test_valid_student_creation():
    """Test that a valid Student object can be created.

    This test creates a Student object with valid data and checks
    whether all given values are stored correctly.
    """

    student = Student(
        student_id="S123",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
    )

    assert student.student_id == "S123"
    assert student.first_name == "Jane"
    assert student.last_name == "Doe"
    assert student.email == "jane.doe@example.com"


# ============================================================
# Test: Full Name Property
# ============================================================

def test_full_name_property():
    """Test that full_name combines first_name and last_name.

    The full_name property should return the first name and last name
    as one readable string.
    """

    student = Student(
        student_id="S123",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
    )

    assert student.full_name == "Jane Doe"


# ============================================================
# Test: Readable String Representation
# ============================================================

def test_readable_string_representation():
    """Test the readable __str__ output of a Student object.

    This test checks whether str(student) returns the expected text.
    The output should contain the full name, student ID, and email address.
    """

    student = Student(
        student_id="S123",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
    )

    assert (
        str(student)
        == "Student: Jane Doe (ID: S123, Email: jane.doe@example.com)"
    )


# ============================================================
# Test: Empty Student ID Validation
# ============================================================

def test_empty_student_id_raises_value_error():
    """Test that an empty student ID raises ValueError.

    A student must always have a student ID.
    This test checks that an empty student ID is rejected during
    object creation.
    """

    with pytest.raises(ValueError):
        Student("", "Jane", "Doe", "jane.doe@example.com")


# ============================================================
# Test: Empty First Name Validation
# ============================================================

def test_empty_first_name_raises_value_error():
    """Test that an empty first name raises ValueError.

    A student must always have a first name.
    This test checks that an empty first name is rejected during
    object creation.
    """

    with pytest.raises(ValueError):
        Student("S123", "", "Doe", "jane.doe@example.com")


# ============================================================
# Test: Empty Last Name Validation
# ============================================================

def test_empty_last_name_raises_value_error():
    """Test that an empty last name raises ValueError.

    A student must always have a last name.
    This test checks that an empty last name is rejected during
    object creation.
    """

    with pytest.raises(ValueError):
        Student("S123", "Jane", "", "jane.doe@example.com")


# ============================================================
# Test: Invalid Email Validation
# ============================================================

def test_invalid_email_raises_value_error():
    """Test that an email address without '@' raises ValueError.

    This project uses a simple email validation rule.
    The email address must contain the '@' character.
    """

    with pytest.raises(ValueError):
        Student("S123", "Jane", "Doe", "jane.doe.example.com")