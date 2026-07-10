"""Student module for the student grade tracker.

This module contains the Student class.
A Student represents one person whose grades are managed in the system.

The class stores basic student information and provides:
- validation after object creation
- a full name property
- readable text output
"""

# ============================================================
# Imports
# ============================================================

from dataclasses import dataclass


# ============================================================
# Data Class: Student
# ============================================================

@dataclass
class Student:
    """Represent one student in the grade tracker.

    A Student object stores the basic information about one student.

    It contains:
    - a unique student ID
    - a first name
    - a last name
    - an email address

    The Student class also validates its own data after creation.
    """

    student_id: str
    first_name: str
    last_name: str
    email: str

    # ========================================================
    # Post Initialization: Validate Student Data
    # ========================================================

    def __post_init__(self) -> None:
        """Validate the student data after object creation.

        This method is called automatically after the dataclass object
        has been created.

        It checks whether:
        - the student ID is not empty
        - the first name is not empty
        - the last name is not empty
        - the email address contains an '@' character

        Raises:
            ValueError: If one of the student values is invalid.
        """

        # The student ID must not be empty or contain only spaces.
        if not self.student_id.strip():
            raise ValueError("student_id cannot be empty.")

        # The first name must not be empty or contain only spaces.
        if not self.first_name.strip():
            raise ValueError("first_name cannot be empty.")

        # The last name must not be empty or contain only spaces.
        if not self.last_name.strip():
            raise ValueError("last_name cannot be empty.")

        # A simple email check: the email address must contain '@'.
        if "@" not in self.email:
            raise ValueError("email must contain '@'.")

    # ========================================================
    # Property: Build Full Name
    # ========================================================

    @property
    def full_name(self) -> str:
        """Return the student's full name.

        This property combines the first name and the last name
        into one readable full name.

        Returns:
            The full name of the student.
        """

        return f"{self.first_name} {self.last_name}"

    # ========================================================
    # String Representation: Show Student as Readable Text
    # ========================================================

    def __str__(self) -> str:
        """Return a readable text representation of the student.

        This method defines how a Student object is shown when it is printed.
        It includes the full name, student ID, and email address.

        Returns:
            A readable string containing the most important student information.
        """

        return (
            f"Student: {self.full_name} "
            f"(ID: {self.student_id}, Email: {self.email})"
        )