"""Start file for the Student Grade Tracker."""

from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.student import Student


def main() -> None:
    """Start a small example run of the Student Grade Tracker."""

    print("Student Grade Tracker started.")
    print("--------------------------------")

    gradebook = GradeBook()

    student = Student(
        student_id="S001",
        first_name="Anna",
        last_name="Schmidt",
        email="anna@example.com",
    )

    course = Course(
        course_id="CS101",
        name="Intro to Computer Science",
    )

    gradebook.add_student(student)
    gradebook.add_course(course)

    grade = gradebook.record_grade(
        student_id="S001",
        course_id="CS101",
        score=85.0,
        date="2026-07-07",
    )

    print("\nStudent:")
    print(student)

    print("\nCourse:")
    print(course)

    print("\nGrade:")
    print(grade)

    print("\nStatistics:")
    print("Student average:", gradebook.student_average("S001"))


if __name__ == "__main__":
    main()