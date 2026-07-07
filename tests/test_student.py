import pytest

from notenverwaltung.student import Student


def test_valid_student_creation():
    """Tests that a valid student object can be created."""

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


def test_full_name_property():
    """Tests that full_name combines first_name and last_name."""

    student = Student(
        student_id="S123",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
    )

    assert student.full_name == "Jane Doe"


def test_readable_string_representation():
    """Tests the readable __str__ output."""

    student = Student(
        student_id="S123",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
    )

    assert str(student) == "Student: Jane Doe (ID: S123, Email: jane.doe@example.com)"


def test_empty_student_id_raises_value_error():
    """Tests that an empty student_id is not allowed."""

    with pytest.raises(ValueError):
        Student("", "Jane", "Doe", "jane.doe@example.com")


def test_empty_first_name_raises_value_error():
    """Tests that an empty first_name is not allowed."""

    with pytest.raises(ValueError):
        Student("S123", "", "Doe", "jane.doe@example.com")


def test_empty_last_name_raises_value_error():
    """Tests that an empty last_name is not allowed."""

    with pytest.raises(ValueError):
        Student("S123", "Jane", "", "jane.doe@example.com")


def test_invalid_email_raises_value_error():
    """Tests that an email without @ is not allowed."""

    with pytest.raises(ValueError):
        Student("S123", "Jane", "Doe", "jane.doe.example.com")