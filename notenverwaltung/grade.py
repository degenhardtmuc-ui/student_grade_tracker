from dataclasses import dataclass
from datetime import datetime

from notenverwaltung.course import Course
from notenverwaltung.student import Student


@dataclass
class Grade:
    """Represents one grade for one student in one course."""

    student: Student
    course: Course
    score: float
    date: str
    notes: str = ""

    def __post_init__(self) -> None:
        """Validates score and date after object creation."""

        if not 0 <= self.score <= self.course.max_grade:
            raise ValueError(
                f"score must be between 0 and {self.course.max_grade}."
            )

        try:
            datetime.fromisoformat(self.date)
        except ValueError:
            raise ValueError("date must be in ISO format, for example: 2026-07-07.")

    @property
    def is_passing(self) -> bool:
        """Returns True if the score reaches the passing grade."""

        return self.score >= self.course.passing_grade

    @property
    def percentage(self) -> float:
        """Returns the score as a percentage of the maximum grade."""

        return self.score / self.course.max_grade * 100

    @property
    def letter_grade(self) -> str:
        """Returns the letter grade based on the percentage."""

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

    def __str__(self) -> str:
        """Returns a readable text representation of the grade."""

        status = "PASSED" if self.is_passing else "FAILED"

        return (
            f"Grade: {self.student.full_name} | "
            f"{self.course.name} | "
            f"Score: {self.score}/{self.course.max_grade} "
            f"({self.letter_grade}) | "
            f"{status}"
        )