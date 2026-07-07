from dataclasses import dataclass


@dataclass
class Course:
    """Represents one course or subject in the grade tracker."""

    course_id: str
    name: str
    max_grade: float = 100.0
    passing_grade: float = 50.0

    def __post_init__(self) -> None:
        """Validates the course data after object creation."""

        if not self.course_id.strip():
            raise ValueError("course_id cannot be empty.")

        if not self.name.strip():
            raise ValueError("name cannot be empty.")

        if self.max_grade <= 0:
            raise ValueError("max_grade must be greater than 0.")

        if self.passing_grade <= 0:
            raise ValueError("passing_grade must be greater than 0.")

        if self.passing_grade > self.max_grade:
            raise ValueError("passing_grade cannot be greater than max_grade.")

    def __str__(self) -> str:
        """Returns a readable text representation of the course."""

        return (
            f"Course: {self.name} "
            f"({self.course_id}) | "
            f"Pass/Max: {self.passing_grade}/{self.max_grade}"
        )