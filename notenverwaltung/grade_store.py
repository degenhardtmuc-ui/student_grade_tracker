"""Storage abstractions for the student grade tracker.

This module separates the GradeBook logic from the place where data is stored.
The GradeStore abstract class defines one common interface.

Two concrete implementations are provided:
- InMemoryGradeStore stores data in dictionaries and a list.
- SqliteGradeStore stores data through GradeDatabase.
"""

# ============================================================
# Imports
# ============================================================

from abc import ABC, abstractmethod

from notenverwaltung.course import Course
from notenverwaltung.database import GradeDatabase
from notenverwaltung.exceptions import (
    CourseNotFoundError,
    DuplicateEntryError,
    PersistenceError,
    StudentNotFoundError,
)
from notenverwaltung.grade import Grade
from notenverwaltung.student import Student


# ============================================================
# Abstract Base Class: Common Storage Interface
# ============================================================

class GradeStore(ABC):
    """Define the common interface for all grade storage classes.

    GradeBook only works with this interface. It does not need to know
    whether the data is stored in Python collections or in SQLite.
    """

    # --------------------------------------------------------
    # Student Methods
    # --------------------------------------------------------

    @abstractmethod
    def add_student(self, student: Student) -> None:
        """Store one new student."""

    @abstractmethod
    def get_student(self, student_id: str) -> Student:
        """Return one student by student ID."""

    @abstractmethod
    def get_all_students(self) -> list[Student]:
        """Return all stored students."""

    @abstractmethod
    def update_student(self, student: Student) -> None:
        """Update one existing student."""

    @abstractmethod
    def delete_student(self, student_id: str) -> None:
        """Delete one existing student."""

    # --------------------------------------------------------
    # Course Methods
    # --------------------------------------------------------

    @abstractmethod
    def add_course(self, course: Course) -> None:
        """Store one new course."""

    @abstractmethod
    def get_course(self, course_id: str) -> Course:
        """Return one course by course ID."""

    @abstractmethod
    def get_all_courses(self) -> list[Course]:
        """Return all stored courses."""

    @abstractmethod
    def update_course(self, course: Course) -> None:
        """Update one existing course."""

    @abstractmethod
    def delete_course(self, course_id: str) -> None:
        """Delete one existing course."""

    # --------------------------------------------------------
    # Grade Methods
    # --------------------------------------------------------

    @abstractmethod
    def record_grade(self, grade: Grade) -> None:
        """Store one new grade."""

    @abstractmethod
    def get_all_grades(self) -> list[Grade]:
        """Return all stored grades."""

    @abstractmethod
    def get_student_grades(self, student_id: str) -> list[Grade]:
        """Return all grades for one student."""

    @abstractmethod
    def get_course_grades(self, course_id: str) -> list[Grade]:
        """Return all grades for one course."""


# ============================================================
# Concrete Store: Python Dictionaries and List
# ============================================================

class InMemoryGradeStore(GradeStore):
    """Store students, courses, and grades in Python collections.

    This class contains the original dictionary-based storage behavior.
    The data exists only while the Python program is running.
    """

    def __init__(self) -> None:
        """Create empty collections for students, courses, and grades."""

        self._students: dict[str, Student] = {}
        self._courses: dict[str, Course] = {}
        self._grades: list[Grade] = []

    # --------------------------------------------------------
    # Student Methods
    # --------------------------------------------------------

    def add_student(self, student: Student) -> None:
        """Store one student and prevent duplicate student IDs."""

        if student.student_id in self._students:
            raise DuplicateEntryError(
                f"Student with ID {student.student_id} already exists."
            )

        self._students[student.student_id] = student

    def get_student(self, student_id: str) -> Student:
        """Return one student or raise StudentNotFoundError."""

        if student_id not in self._students:
            raise StudentNotFoundError(
                f"Student with ID {student_id} does not exist."
            )

        return self._students[student_id]

    def get_all_students(self) -> list[Student]:
        """Return a new list containing all stored students."""

        return list(self._students.values())

    def update_student(self, student: Student) -> None:
        """Replace one existing student object."""

        self.get_student(student.student_id)
        self._students[student.student_id] = student

        for grade in self._grades:
            if grade.student.student_id == student.student_id:
                grade.student = student

    def delete_student(self, student_id: str) -> None:
        """Delete a student if no grades refer to that student."""

        self.get_student(student_id)

        if any(
            grade.student.student_id == student_id
            for grade in self._grades
        ):
            raise PersistenceError(
                f"Could not delete student {student_id} because grades exist."
            )

        del self._students[student_id]

    # --------------------------------------------------------
    # Course Methods
    # --------------------------------------------------------

    def add_course(self, course: Course) -> None:
        """Store one course and prevent duplicate course IDs."""

        if course.course_id in self._courses:
            raise DuplicateEntryError(
                f"Course with ID {course.course_id} already exists."
            )

        self._courses[course.course_id] = course

    def get_course(self, course_id: str) -> Course:
        """Return one course or raise CourseNotFoundError."""

        if course_id not in self._courses:
            raise CourseNotFoundError(
                f"Course with ID {course_id} does not exist."
            )

        return self._courses[course_id]

    def get_all_courses(self) -> list[Course]:
        """Return a new list containing all stored courses."""

        return list(self._courses.values())

    def update_course(self, course: Course) -> None:
        """Replace one existing course object."""

        self.get_course(course.course_id)
        self._courses[course.course_id] = course

        for grade in self._grades:
            if grade.course.course_id == course.course_id:
                grade.course = course

    def delete_course(self, course_id: str) -> None:
        """Delete a course if no grades refer to that course."""

        self.get_course(course_id)

        if any(
            grade.course.course_id == course_id
            for grade in self._grades
        ):
            raise PersistenceError(
                f"Could not delete course {course_id} because grades exist."
            )

        del self._courses[course_id]

    # --------------------------------------------------------
    # Grade Methods
    # --------------------------------------------------------

    def record_grade(self, grade: Grade) -> None:
        """Store one grade after checking its student and course."""

        self.get_student(grade.student.student_id)
        self.get_course(grade.course.course_id)
        self._grades.append(grade)

    def get_all_grades(self) -> list[Grade]:
        """Return a defensive copy of the complete grade list."""

        return list(self._grades)

    def get_student_grades(self, student_id: str) -> list[Grade]:
        """Return a new list with all grades for one student."""

        self.get_student(student_id)

        return [
            grade
            for grade in self._grades
            if grade.student.student_id == student_id
        ]

    def get_course_grades(self, course_id: str) -> list[Grade]:
        """Return a new list with all grades for one course."""

        self.get_course(course_id)

        return [
            grade
            for grade in self._grades
            if grade.course.course_id == course_id
        ]


# ============================================================
# Concrete Store: SQLite Database
# ============================================================

class SqliteGradeStore(GradeStore):
    """Store grade tracker data through a GradeDatabase object.

    This class is an adapter. It translates calls from the GradeStore
    interface into calls to the SQLite database implementation.
    """

    def __init__(self, database: GradeDatabase) -> None:
        """Store the database object used for all operations."""

        self.database = database

    # --------------------------------------------------------
    # Student Methods
    # --------------------------------------------------------

    def add_student(self, student: Student) -> None:
        """Store one student in SQLite."""

        self.database.add_student(student)

    def get_student(self, student_id: str) -> Student:
        """Return one student from SQLite."""

        return self.database.get_student(student_id)

    def get_all_students(self) -> list[Student]:
        """Return all students from SQLite."""

        return self.database.get_all_students()

    def update_student(self, student: Student) -> None:
        """Update one student in SQLite."""

        self.database.update_student(student)

    def delete_student(self, student_id: str) -> None:
        """Delete one student from SQLite."""

        self.database.delete_student(student_id)

    # --------------------------------------------------------
    # Course Methods
    # --------------------------------------------------------

    def add_course(self, course: Course) -> None:
        """Store one course in SQLite."""

        self.database.add_course(course)

    def get_course(self, course_id: str) -> Course:
        """Return one course from SQLite."""

        return self.database.get_course(course_id)

    def get_all_courses(self) -> list[Course]:
        """Return all courses from SQLite."""

        return self.database.get_all_courses()

    def update_course(self, course: Course) -> None:
        """Update one course in SQLite."""

        self.database.update_course(course)

    def delete_course(self, course_id: str) -> None:
        """Delete one course from SQLite."""

        self.database.delete_course(course_id)

    # --------------------------------------------------------
    # Grade Methods
    # --------------------------------------------------------

    def record_grade(self, grade: Grade) -> None:
        """Store one grade in SQLite."""

        self.database.record_grade(grade)

    def get_all_grades(self) -> list[Grade]:
        """Return all grades from SQLite."""

        return self.database.get_all_grades()

    def get_student_grades(self, student_id: str) -> list[Grade]:
        """Return one student's grades from SQLite."""

        return self.database.get_student_grades(student_id)

    def get_course_grades(self, course_id: str) -> list[Grade]:
        """Return one course's grades from SQLite."""

        return self.database.get_course_grades(course_id)
