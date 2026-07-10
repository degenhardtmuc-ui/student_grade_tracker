"""Course module for the student grade tracker.

This module contains the Course class.
A Course represents one school subject, university course, or learning unit
inside the grade management system.
"""

# ============================================================
# Imports
# ============================================================

from dataclasses import dataclass


# ============================================================
# Data Class: Course
# ============================================================

@dataclass
class Course:
    """Represent one course or subject in the grade tracker.

    A Course object stores the basic information about a course.

    It contains:
    - a unique course ID
    - a course name
    - the maximum possible grade
    - the minimum grade needed to pass

    The Course class also validates its own data after creation.
    """

    course_id: str
    name: str
    max_grade: float = 100.0
    passing_grade: float = 50.0

    # ========================================================
    # Post Initialization: Validate Course Data
    # ========================================================

    def __post_init__(self) -> None:
        """Validate the course data after object creation.

        This method is called automatically after the dataclass object
        has been created.

        It checks whether:
        - the course ID is not empty
        - the course name is not empty
        - the maximum grade is greater than zero
        - the passing grade is greater than zero
        - the passing grade is not greater than the maximum grade

        Raises:
            ValueError: If one of the course values is invalid.
        """

        # The course ID must not be empty or contain only spaces.
        if not self.course_id.strip():
            raise ValueError("course_id cannot be empty.")

        # The course name must not be empty or contain only spaces.
        if not self.name.strip():
            raise ValueError("name cannot be empty.")

        # The maximum grade must be greater than zero.
        if self.max_grade <= 0:
            raise ValueError("max_grade must be greater than 0.")

        # The passing grade must be greater than zero.
        if self.passing_grade <= 0:
            raise ValueError("passing_grade must be greater than 0.")

        # The passing grade cannot be higher than the maximum grade.
        if self.passing_grade > self.max_grade:
            raise ValueError("passing_grade cannot be greater than max_grade.")

    # ========================================================
    # String Representation: Show Course as Readable Text
    # ========================================================

    def __str__(self) -> str:
        """Return a readable text representation of the course.

        This method defines how a Course object is shown when it is printed.
        It makes the output easier to understand for users.

        Returns:
            A readable string containing the course name, course ID,
            passing grade, and maximum grade.
        """

        return (
            f"Course: {self.name} "
            f"({self.course_id}) | "
            f"Pass/Max: {self.passing_grade}/{self.max_grade}"
        )