"""Grade module for the student grade tracker.

This module contains the Grade class.
A Grade represents one score that belongs to one student and one course.

The class also provides helpful calculated properties, such as:
- pass or fail status
- percentage value
- letter grade
- readable text output
"""

# ============================================================
# Imports
# ============================================================

from dataclasses import dataclass
from datetime import datetime

from notenverwaltung.course import Course
from notenverwaltung.student import Student


# ============================================================
# Data Class: Grade
# ============================================================

@dataclass
class Grade:
    """Represent one grade for one student in one course.

    A Grade object connects three important pieces of information:
    - the student who received the grade
    - the course where the grade was recorded
    - the score that was achieved

    It also stores the date of the grade and optional notes.
    """

    student: Student
    course: Course
    score: float
    date: str
    notes: str = ""

    # ========================================================
    # Post Initialization: Validate Grade Data
    # ========================================================

    def __post_init__(self) -> None:
        """Validate the grade data after object creation.

        This method is called automatically after the dataclass object
        has been created.

        It checks whether:
        - the score is not below zero
        - the score is not higher than the course maximum grade
        - the date is written in ISO format

        Example for a valid ISO date:
        2026-07-07

        Raises:
            ValueError: If the score or date is invalid.
        """

        # The score must be between 0 and the maximum grade of the course.
        if not 0 <= self.score <= self.course.max_grade:
            raise ValueError(
                f"score must be between 0 and {self.course.max_grade}."
            )

        # The date must be a valid ISO date, for example: 2026-07-07.
        try:
            datetime.fromisoformat(self.date)
        except ValueError:
            raise ValueError(
                "date must be in ISO format, for example: 2026-07-07."
            )

    # ========================================================
    # Property: Check Passing Status
    # ========================================================

    @property
    def is_passing(self) -> bool:
        """Return True if the score reaches the passing grade.

        This property compares the score with the passing grade of the
        related course.

        Returns:
            True if the student passed the course, otherwise False.
        """

        return self.score >= self.course.passing_grade

    # ========================================================
    # Property: Calculate Percentage
    # ========================================================

    @property
    def percentage(self) -> float:
        """Return the score as a percentage of the maximum grade.

        This property converts the raw score into a percentage value.
        This makes grades from different courses easier to compare.

        Returns:
            The score as a percentage.
        """

        return self.score / self.course.max_grade * 100

    # ========================================================
    # Property: Calculate Letter Grade
    # ========================================================

    @property
    def letter_grade(self) -> str:
        """Return the letter grade based on the percentage.

        The percentage value is converted into a simple letter grade.

        The grading scale is:
        - A: 90 percent or higher
        - B: 80 percent or higher
        - C: 70 percent or higher
        - D: 60 percent or higher
        - F: below 60 percent

        Returns:
            The letter grade as a string.
        """

        percentage = self.percentage

        if percentage >= 90:
            return "A"

        if percentage >= 80:
            return "B"

        if percentage >= 70:
            return "C"

        if percentage >= 60:
            return "D"

        return "F"

    # ========================================================
    # String Representation: Show Grade as Readable Text
    # ========================================================

    def __str__(self) -> str:
        """Return a readable text representation of the grade.

        This method defines how a Grade object is shown when it is printed.
        It includes the student name, course name, score, letter grade,
        and pass or fail status.

        Returns:
            A readable string containing the most important grade information.
        """

        status = "PASSED" if self.is_passing else "FAILED"

        return (
            f"Grade: {self.student.full_name} | "
            f"{self.course.name} | "
            f"Score: {self.score}/{self.course.max_grade} "
            f"({self.letter_grade}) | "
            f"{status}"
        )