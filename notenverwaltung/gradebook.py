"""Main GradeBook management module for the student grade system.

This module contains the GradeBook class. The GradeBook works as the
central manager of the application.

It manages:
- students
- courses
- grades
- grade statistics
- search functions
- JSON saving and loading
- CSV export and import
- selectable in-memory or SQLite storage

The goal of this module is to provide clear methods for working with
grade book data while a GradeStore handles the actual storage.
"""

# ============================================================
# Imports
# ============================================================

import json
import re
from pathlib import Path

from notenverwaltung.course import Course
from notenverwaltung.exceptions import PersistenceError
from notenverwaltung.grade import Grade
from notenverwaltung.grade_store import GradeStore, InMemoryGradeStore
from notenverwaltung.student import Student


# ============================================================
# Main Class: GradeBook Management
# ============================================================

class GradeBook:
    """Manage students, courses, grades, statistics, and file operations.

    The GradeBook class is the central class of the application.
    It coordinates all students, courses, and recorded grades.
    A GradeStore object handles the actual data storage.

    It also provides methods to:
    - add students and courses
    - record grades
    - calculate averages
    - calculate course pass rates
    - find top students
    - find students at risk
    - search students and courses
    - save and load data as JSON
    - export and import grades as CSV
    """

    # ========================================================
    # Initialization: Create an Empty GradeBook
    # ========================================================

    def __init__(self, store: GradeStore | None = None) -> None:
        """Create a GradeBook with a selectable storage implementation.

        Args:
            store: Storage object used for students, courses, and grades.
                If no store is provided, InMemoryGradeStore is used.

        Dependency injection makes it possible to use the same GradeBook
        logic with Python collections or with a SQLite database.
        """

        self.store = store if store is not None else InMemoryGradeStore()

    # ========================================================
    # Storage Properties: Read Complete Collections
    # ========================================================

    @property
    def students(self) -> dict[str, Student]:
        """Return all students as a dictionary keyed by student ID."""

        return {
            student.student_id: student
            for student in self.store.get_all_students()
        }

    @property
    def courses(self) -> dict[str, Course]:
        """Return all courses as a dictionary keyed by course ID."""

        return {
            course.course_id: course
            for course in self.store.get_all_courses()
        }

    @property
    def grades(self) -> list[Grade]:
        """Return a defensive copy of all stored grades."""

        return self.store.get_all_grades()

    # ========================================================
    # Student Management: Add Students
    # ========================================================

    def add_student(self, student: Student) -> None:
        """Add one student to the GradeBook.

        The student is stored by student ID.

        If a student with the same ID already exists, a
        DuplicateEntryError is raised. This prevents duplicate
        students in the GradeBook.
        """

        self.store.add_student(student)

    # ========================================================
    # Course Management: Add Courses
    # ========================================================

    def add_course(self, course: Course) -> None:
        """Add one course to the GradeBook.

        The course is stored by course ID.

        If a course with the same ID already exists, a
        DuplicateEntryError is raised. This prevents duplicate
        courses in the GradeBook.
        """

        self.store.add_course(course)

    # ========================================================
    # Grade Management: Record Grades
    # ========================================================

    def record_grade(
        self,
        student_id: str,
        course_id: str,
        score: float,
        date: str,
        notes: str = "",
    ) -> Grade:
        """Create and store one grade for an existing student and course.

        The method first checks whether the student and the course exist.
        If both exist, a new Grade object is created and added to the
        internal grades list.

        Args:
            student_id: The ID of the student who receives the grade.
            course_id: The ID of the course for this grade.
            score: The achieved score.
            date: The date when the grade was recorded.
            notes: Optional notes for the grade.

        Returns:
            The newly created Grade object.

        Raises:
            StudentNotFoundError: If the student ID does not exist.
            CourseNotFoundError: If the course ID does not exist.
        """

        student = self.store.get_student(student_id)
        course = self.store.get_course(course_id)

        grade = Grade(
            student=student,
            course=course,
            score=score,
            date=date,
            notes=notes,
        )

        self.store.record_grade(grade)

        return grade

    # ========================================================
    # Grade Lookup: Get Grades by Student
    # ========================================================

    def get_student_grades(self, student_id: str) -> list[Grade]:
        """Return all grades for one student.

        The method searches the internal grades list and returns only
        the grades that belong to the given student ID.

        Args:
            student_id: The ID of the student.

        Returns:
            A list of Grade objects for the selected student.

        Raises:
            StudentNotFoundError: If the student ID does not exist.
        """

        return self.store.get_student_grades(student_id)

    # ========================================================
    # Grade Lookup: Get Grades by Course
    # ========================================================

    def get_course_grades(self, course_id: str) -> list[Grade]:
        """Return all grades for one course.

        The method searches the internal grades list and returns only
        the grades that belong to the given course ID.

        Args:
            course_id: The ID of the course.

        Returns:
            A list of Grade objects for the selected course.

        Raises:
            CourseNotFoundError: If the course ID does not exist.
        """

        return self.store.get_course_grades(course_id)

    # ========================================================
    # Statistics: Calculate Student Average
    # ========================================================

    def student_average(self, student_id: str) -> float:
        """Return the average percentage for one student.

        The method gets all grades for the selected student and calculates
        the average percentage.

        Args:
            student_id: The ID of the student.

        Returns:
            The average percentage of the student.

        Raises:
            StudentNotFoundError: If the student ID does not exist.
            ValueError: If the student has no recorded grades.
        """

        grades = self.get_student_grades(student_id)

        if not grades:
            raise ValueError(f"No grades recorded for student {student_id}.")

        total_percentage = sum(grade.percentage for grade in grades)

        return total_percentage / len(grades)

    # ========================================================
    # Statistics: Calculate Course Average
    # ========================================================

    def course_average(self, course_id: str) -> float:
        """Return the average score for one course.

        The method gets all grades for the selected course and calculates
        the average score.

        Args:
            course_id: The ID of the course.

        Returns:
            The average score of the course.

        Raises:
            CourseNotFoundError: If the course ID does not exist.
            ValueError: If the course has no recorded grades.
        """

        grades = self.get_course_grades(course_id)

        if not grades:
            raise ValueError(f"No grades recorded for course {course_id}.")

        total_score = sum(grade.score for grade in grades)

        return total_score / len(grades)

    # ========================================================
    # Statistics: Calculate Course Pass Rate
    # ========================================================

    def course_pass_rate(self, course_id: str) -> float:
        """Return the percentage of passing grades for one course.

        The method checks how many grades in a course are passing grades.
        Then it calculates the pass rate as a percentage.

        Args:
            course_id: The ID of the course.

        Returns:
            The pass rate of the course in percent.

        Raises:
            CourseNotFoundError: If the course ID does not exist.
            ValueError: If the course has no recorded grades.
        """

        grades = self.get_course_grades(course_id)

        if not grades:
            raise ValueError(f"No grades recorded for course {course_id}.")

        passing_grades = 0

        for grade in grades:
            if grade.is_passing:
                passing_grades = passing_grades + 1

        return passing_grades / len(grades) * 100

    # ========================================================
    # Ranking: Find Top Students
    # ========================================================

    def top_students(self, n: int = 5) -> list[tuple[Student, float]]:
        """Return the top N students by average percentage.

        The method calculates the average for every student who has
        at least one recorded grade. Then it sorts the students from
        the highest average to the lowest average.

        Args:
            n: The maximum number of top students to return.

        Returns:
            A list of tuples. Each tuple contains a Student object and
            the student's average percentage.
        """

        averages = []

        for student_id, student in self.students.items():
            student_grades = self.get_student_grades(student_id)

            if student_grades:
                average = self.student_average(student_id)
                averages.append((student, average))

        averages.sort(key=lambda item: item[1], reverse=True)

        return averages[:n]

    # ========================================================
    # Risk Analysis: Find Students Below a Threshold
    # ========================================================

    def students_at_risk(self, threshold: float = 60.0) -> list[Student]:
        """Return students whose average percentage is below the threshold.

        This method can be used to find students who may need support.
        Only students with at least one recorded grade are checked.

        Args:
            threshold: The percentage limit below which a student is
                considered at risk.

        Returns:
            A list of Student objects whose average is below the threshold.
        """

        at_risk_students = []

        for student_id, student in self.students.items():
            student_grades = self.get_student_grades(student_id)

            if student_grades:
                average = self.student_average(student_id)

                if average < threshold:
                    at_risk_students.append(student)

        return at_risk_students

    # ========================================================
    # Search Functions: Search Students
    # ========================================================

    def search_students(self, query: str) -> list[Student]:
        """Search students by first name, last name, email, or full name.

        The search uses a regular expression. The search is not
        case-sensitive, so uppercase and lowercase letters do not matter.

        Args:
            query: The search text or regular expression.

        Returns:
            A list of matching Student objects.
        """

        pattern = re.compile(query, re.IGNORECASE)

        return [
            student
            for student in self.students.values()
            if pattern.search(student.first_name)
            or pattern.search(student.last_name)
            or pattern.search(student.email)
            or pattern.search(student.full_name)
        ]

    # ========================================================
    # Search Functions: Search Courses
    # ========================================================

    def search_courses(self, query: str) -> list[Course]:
        """Search courses by course name.

        The search uses a regular expression. The search is not
        case-sensitive, so uppercase and lowercase letters do not matter.

        Args:
            query: The search text or regular expression.

        Returns:
            A list of matching Course objects.
        """

        pattern = re.compile(query, re.IGNORECASE)

        return [
            course
            for course in self.courses.values()
            if pattern.search(course.name)
        ]

    # ========================================================
    # JSON Persistence: Convert GradeBook to Dictionary
    # ========================================================

    def to_dict(self) -> dict:
        """Convert the complete GradeBook into simple dictionary data.

        This method prepares the GradeBook for JSON saving.

        Complex objects like Student, Course, and Grade are converted
        into dictionaries with simple values such as strings, numbers,
        and lists.

        Returns:
            A dictionary containing students, courses, and grades.
        """

        students_data = []

        for student in self.students.values():
            students_data.append(
                {
                    "student_id": student.student_id,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "email": student.email,
                }
            )

        courses_data = []

        for course in self.courses.values():
            courses_data.append(
                {
                    "course_id": course.course_id,
                    "name": course.name,
                    "max_grade": course.max_grade,
                    "passing_grade": course.passing_grade,
                }
            )

        grades_data = []

        for grade in self.grades:
            grades_data.append(
                {
                    "student_id": grade.student.student_id,
                    "course_id": grade.course.course_id,
                    "score": grade.score,
                    "date": grade.date,
                    "notes": grade.notes,
                }
            )

        return {
            "students": students_data,
            "courses": courses_data,
            "grades": grades_data,
        }

    # ========================================================
    # JSON Persistence: Rebuild GradeBook from Dictionary
    # ========================================================

    @classmethod
    def from_dict(cls, data: dict) -> "GradeBook":
        """Create a GradeBook object from dictionary data.

        This method rebuilds students, courses, and grades from simple
        Python dictionary data.

        It is mainly used after loading JSON data from a file.

        Args:
            data: Dictionary data containing students, courses, and grades.

        Returns:
            A rebuilt GradeBook object.

        Raises:
            KeyError: If required dictionary keys are missing.
            ValueError: If the loaded data contains invalid values.
        """

        gradebook = cls()

        for student_data in data["students"]:
            student = Student(
                student_id=student_data["student_id"],
                first_name=student_data["first_name"],
                last_name=student_data["last_name"],
                email=student_data["email"],
            )

            gradebook.add_student(student)

        for course_data in data["courses"]:
            course = Course(
                course_id=course_data["course_id"],
                name=course_data["name"],
                max_grade=course_data["max_grade"],
                passing_grade=course_data["passing_grade"],
            )

            gradebook.add_course(course)

        for grade_data in data["grades"]:
            gradebook.record_grade(
                student_id=grade_data["student_id"],
                course_id=grade_data["course_id"],
                score=grade_data["score"],
                date=grade_data["date"],
                notes=grade_data.get("notes", ""),
            )

        return gradebook

    # ========================================================
    # JSON Persistence: Save GradeBook as JSON File
    # ========================================================

    def save_json(self, file_path: str) -> None:
        """Save the complete GradeBook as a JSON file.

        The method first converts the GradeBook into dictionary data.
        Then it converts this data into formatted JSON text and writes
        it into the selected file.

        Args:
            file_path: The path where the JSON file should be saved.

        Raises:
            PersistenceError: If the file cannot be written.
        """

        try:
            path = Path(file_path)
            data = self.to_dict()

            json_text = json.dumps(data, indent=4)
            path.write_text(json_text, encoding="utf-8")

        except OSError as error:
            raise PersistenceError(
                f"Could not save JSON file: {file_path}"
            ) from error

    # ========================================================
    # JSON Persistence: Load GradeBook from JSON File
    # ========================================================

    @classmethod
    def load_json(cls, file_path: str) -> "GradeBook":
        """Load a GradeBook object from a JSON file.

        The method reads JSON text from a file, converts it into
        dictionary data, and rebuilds a GradeBook object from this data.

        Args:
            file_path: The path of the JSON file that should be loaded.

        Returns:
            A loaded GradeBook object.

        Raises:
            PersistenceError: If the file cannot be read, decoded,
            or converted into valid GradeBook data.
        """

        try:
            path = Path(file_path)
            json_text = path.read_text(encoding="utf-8")
            data = json.loads(json_text)

            return cls.from_dict(data)

        except OSError as error:
            raise PersistenceError(
                f"Could not read JSON file: {file_path}"
            ) from error

        except json.JSONDecodeError as error:
            raise PersistenceError(
                f"Could not decode JSON file: {file_path}"
            ) from error

        except (KeyError, TypeError, ValueError) as error:
            raise PersistenceError(
                f"JSON file contains invalid grade book data: {file_path}"
            ) from error

    # ========================================================
    # CSV Export: Export Grades to CSV File
    # ========================================================

    def export_grades_to_csv(self, file_path: str) -> None:
        """Export all recorded grades into a simple CSV file.

        The CSV file contains one header row and one row for each grade.
        Each row stores the student ID, course ID, score, and date.

        Args:
            file_path: The path where the CSV file should be saved.

        Raises:
            PersistenceError: If the CSV file cannot be written.
        """

        try:
            path = Path(file_path)

            lines = ["student_id,course_id,score,date"]

            for grade in self.grades:
                line = (
                    f"{grade.student.student_id},"
                    f"{grade.course.course_id},"
                    f"{grade.score},"
                    f"{grade.date}"
                )

                lines.append(line)

            csv_text = "\n".join(lines)
            path.write_text(csv_text, encoding="utf-8")

        except OSError as error:
            raise PersistenceError(
                f"Could not write CSV file: {file_path}"
            ) from error

    # ========================================================
    # CSV Import: Import Grades from CSV File
    # ========================================================

    def import_grades_from_csv(self, file_path: str) -> dict:
        """Import grades from a CSV file and return an import report.

        The method reads a CSV file line by line.
        Valid lines are converted into Grade objects.
        Invalid lines are skipped and stored in the error report.

        The returned report contains:
        - imported: number of successfully imported grades
        - skipped: number of skipped lines
        - errors: list of error messages

        Args:
            file_path: The path of the CSV file that should be imported.

        Returns:
            A dictionary with import statistics and error messages.

        Raises:
            PersistenceError: If the CSV file cannot be read.
        """

        try:
            path = Path(file_path)
            lines = path.read_text(encoding="utf-8").splitlines()

        except OSError as error:
            raise PersistenceError(
                f"Could not read CSV file: {file_path}"
            ) from error

        report = {
            "imported": 0,
            "skipped": 0,
            "errors": [],
        }

        pattern = re.compile(
            r"^([^,]+),([^,]+),([0-9]+(?:\.[0-9]+)?),(\d{4}-\d{2}-\d{2})$"
        )

        for line_number, line in enumerate(lines, start=1):
            if line_number == 1 and line == "student_id,course_id,score,date":
                continue

            match = pattern.match(line)

            if not match:
                report["skipped"] = report["skipped"] + 1
                report["errors"].append(f"Line {line_number}: invalid format")
                continue

            student_id = match.group(1)
            course_id = match.group(2)
            score = float(match.group(3))
            date = match.group(4)

            try:
                self.record_grade(
                    student_id=student_id,
                    course_id=course_id,
                    score=score,
                    date=date,
                )

                report["imported"] = report["imported"] + 1

            except ValueError as error:
                report["skipped"] = report["skipped"] + 1
                report["errors"].append(f"Line {line_number}: {error}")

        return report
