"""SQLite database module for the student grade tracker.

This module contains the GradeDatabase class.
The class creates the relational database schema and provides methods
for storing, reading, updating, and deleting students, courses, and grades.

It also calculates grade statistics directly with SQL.
"""

# ============================================================
# Imports
# ============================================================

import sqlite3
from pathlib import Path

from notenverwaltung.course import Course
from notenverwaltung.exceptions import (
    CourseNotFoundError,
    DuplicateEntryError,
    PersistenceError,
    StudentNotFoundError,
)
from notenverwaltung.grade import Grade
from notenverwaltung.student import Student


# ============================================================
# Main Class: SQLite Database Management
# ============================================================

class GradeDatabase:
    """Manage all grade tracker data inside a SQLite database.

    The database contains three related tables:
    - students
    - courses
    - grades

    Student and course IDs are primary keys. Every grade stores the IDs
    of its related student and course as foreign keys.
    """

    def __init__(self, database_path: str | Path = "grade_tracker.db") -> None:
        """Open the database connection and create all required tables.

        Args:
            database_path: Path of the SQLite database file. The special
                value ``:memory:`` creates a temporary database in memory.

        Raises:
            PersistenceError: If the database cannot be opened or prepared.
        """

        self.database_path = str(database_path)

        try:
            self.connection = sqlite3.connect(self.database_path)
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.create_tables()
        except sqlite3.Error as error:
            raise PersistenceError(
                f"Could not open SQLite database: {self.database_path}"
            ) from error

    # ========================================================
    # Database Schema: Create Tables
    # ========================================================

    def create_tables(self) -> None:
        """Create the students, courses, and grades tables.

        ``IF NOT EXISTS`` prevents an error when an existing database is
        opened again. Existing data is not deleted or overwritten.

        Raises:
            PersistenceError: If the tables cannot be created.
        """

        schema = """
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            max_grade REAL NOT NULL DEFAULT 100.0,
            passing_grade REAL NOT NULL DEFAULT 50.0
        );

        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            score REAL NOT NULL,
            date TEXT NOT NULL,
            notes TEXT DEFAULT '',
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        );
        """

        try:
            self.connection.executescript(schema)
            self.connection.commit()
        except sqlite3.Error as error:
            raise PersistenceError("Could not create database tables.") from error

    # ========================================================
    # Student CRUD: Create
    # ========================================================

    def add_student(self, student: Student) -> None:
        """Insert one student into the students table.

        Args:
            student: Student object that should be stored.

        Raises:
            DuplicateEntryError: If the student ID already exists.
            PersistenceError: If the database operation fails.
        """

        sql = """
        INSERT INTO students (student_id, first_name, last_name, email)
        VALUES (?, ?, ?, ?)
        """

        try:
            with self.connection:
                self.connection.execute(
                    sql,
                    (
                        student.student_id,
                        student.first_name,
                        student.last_name,
                        student.email,
                    ),
                )
        except sqlite3.IntegrityError as error:
            raise DuplicateEntryError(
                f"Student with ID {student.student_id} already exists."
            ) from error
        except sqlite3.Error as error:
            raise PersistenceError("Could not add student to database.") from error

    # ========================================================
    # Student CRUD: Read
    # ========================================================

    def get_student(self, student_id: str) -> Student:
        """Return one student from the database by student ID.

        Raises:
            StudentNotFoundError: If the student ID does not exist.
        """

        row = self.connection.execute(
            """
            SELECT student_id, first_name, last_name, email
            FROM students
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()

        if row is None:
            raise StudentNotFoundError(
                f"Student with ID {student_id} does not exist."
            )

        return self._row_to_student(row)

    def get_all_students(self) -> list[Student]:
        """Return all stored students ordered by student ID."""

        rows = self.connection.execute(
            """
            SELECT student_id, first_name, last_name, email
            FROM students
            ORDER BY student_id
            """
        ).fetchall()

        return [self._row_to_student(row) for row in rows]

    # ========================================================
    # Student CRUD: Update
    # ========================================================

    def update_student(self, student: Student) -> None:
        """Update the name and email of an existing student.

        Raises:
            StudentNotFoundError: If the student ID does not exist.
            PersistenceError: If the database operation fails.
        """

        self.get_student(student.student_id)

        try:
            with self.connection:
                self.connection.execute(
                    """
                    UPDATE students
                    SET first_name = ?, last_name = ?, email = ?
                    WHERE student_id = ?
                    """,
                    (
                        student.first_name,
                        student.last_name,
                        student.email,
                        student.student_id,
                    ),
                )
        except sqlite3.Error as error:
            raise PersistenceError("Could not update student in database.") from error

    # ========================================================
    # Student CRUD: Delete
    # ========================================================

    def delete_student(self, student_id: str) -> None:
        """Delete an existing student without recorded grades.

        Raises:
            StudentNotFoundError: If the student ID does not exist.
            PersistenceError: If grades still refer to the student or the
                database operation fails.
        """

        self.get_student(student_id)

        try:
            with self.connection:
                self.connection.execute(
                    "DELETE FROM students WHERE student_id = ?",
                    (student_id,),
                )
        except sqlite3.IntegrityError as error:
            raise PersistenceError(
                f"Could not delete student {student_id} because grades exist."
            ) from error
        except sqlite3.Error as error:
            raise PersistenceError("Could not delete student from database.") from error

    # ========================================================
    # Course CRUD: Create
    # ========================================================

    def add_course(self, course: Course) -> None:
        """Insert one course into the courses table.

        Raises:
            DuplicateEntryError: If the course ID already exists.
            PersistenceError: If the database operation fails.
        """

        sql = """
        INSERT INTO courses (course_id, name, max_grade, passing_grade)
        VALUES (?, ?, ?, ?)
        """

        try:
            with self.connection:
                self.connection.execute(
                    sql,
                    (
                        course.course_id,
                        course.name,
                        course.max_grade,
                        course.passing_grade,
                    ),
                )
        except sqlite3.IntegrityError as error:
            raise DuplicateEntryError(
                f"Course with ID {course.course_id} already exists."
            ) from error
        except sqlite3.Error as error:
            raise PersistenceError("Could not add course to database.") from error

    # ========================================================
    # Course CRUD: Read
    # ========================================================

    def get_course(self, course_id: str) -> Course:
        """Return one course from the database by course ID.

        Raises:
            CourseNotFoundError: If the course ID does not exist.
        """

        row = self.connection.execute(
            """
            SELECT course_id, name, max_grade, passing_grade
            FROM courses
            WHERE course_id = ?
            """,
            (course_id,),
        ).fetchone()

        if row is None:
            raise CourseNotFoundError(
                f"Course with ID {course_id} does not exist."
            )

        return self._row_to_course(row)

    def get_all_courses(self) -> list[Course]:
        """Return all stored courses ordered by course ID."""

        rows = self.connection.execute(
            """
            SELECT course_id, name, max_grade, passing_grade
            FROM courses
            ORDER BY course_id
            """
        ).fetchall()

        return [self._row_to_course(row) for row in rows]

    # ========================================================
    # Course CRUD: Update
    # ========================================================

    def update_course(self, course: Course) -> None:
        """Update the data of an existing course.

        Raises:
            CourseNotFoundError: If the course ID does not exist.
            PersistenceError: If the database operation fails.
        """

        self.get_course(course.course_id)

        try:
            with self.connection:
                self.connection.execute(
                    """
                    UPDATE courses
                    SET name = ?, max_grade = ?, passing_grade = ?
                    WHERE course_id = ?
                    """,
                    (
                        course.name,
                        course.max_grade,
                        course.passing_grade,
                        course.course_id,
                    ),
                )
        except sqlite3.Error as error:
            raise PersistenceError("Could not update course in database.") from error

    # ========================================================
    # Course CRUD: Delete
    # ========================================================

    def delete_course(self, course_id: str) -> None:
        """Delete an existing course without recorded grades.

        Raises:
            CourseNotFoundError: If the course ID does not exist.
            PersistenceError: If grades still refer to the course or the
                database operation fails.
        """

        self.get_course(course_id)

        try:
            with self.connection:
                self.connection.execute(
                    "DELETE FROM courses WHERE course_id = ?",
                    (course_id,),
                )
        except sqlite3.IntegrityError as error:
            raise PersistenceError(
                f"Could not delete course {course_id} because grades exist."
            ) from error
        except sqlite3.Error as error:
            raise PersistenceError("Could not delete course from database.") from error

    # ========================================================
    # Grade CRUD: Create
    # ========================================================

    def record_grade(self, grade: Grade) -> int:
        """Insert one grade and return its automatically created ID.

        The method checks the related student and course before the grade
        is inserted. This gives clear custom exceptions for missing IDs.

        Raises:
            StudentNotFoundError: If the related student does not exist.
            CourseNotFoundError: If the related course does not exist.
            PersistenceError: If the database operation fails.
        """

        self.get_student(grade.student.student_id)
        self.get_course(grade.course.course_id)

        try:
            with self.connection:
                cursor = self.connection.execute(
                    """
                    INSERT INTO grades (student_id, course_id, score, date, notes)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        grade.student.student_id,
                        grade.course.course_id,
                        grade.score,
                        grade.date,
                        grade.notes,
                    ),
                )
        except sqlite3.Error as error:
            raise PersistenceError("Could not record grade in database.") from error

        return int(cursor.lastrowid)

    # ========================================================
    # Grade CRUD: Read
    # ========================================================

    def get_grade(self, grade_id: int) -> Grade:
        """Return one grade by its database ID.

        Raises:
            ValueError: If the grade ID does not exist.
        """

        row = self.connection.execute(
            self._grade_select_sql() + " WHERE g.id = ?",
            (grade_id,),
        ).fetchone()

        if row is None:
            raise ValueError(f"Grade with ID {grade_id} does not exist.")

        return self._row_to_grade(row)

    def get_all_grades(self) -> list[Grade]:
        """Return all stored grades ordered by database ID."""

        rows = self.connection.execute(
            self._grade_select_sql() + " ORDER BY g.id"
        ).fetchall()

        return [self._row_to_grade(row) for row in rows]

    def get_student_grades(self, student_id: str) -> list[Grade]:
        """Return all grades for one existing student."""

        self.get_student(student_id)

        rows = self.connection.execute(
            self._grade_select_sql() + " WHERE g.student_id = ? ORDER BY g.id",
            (student_id,),
        ).fetchall()

        return [self._row_to_grade(row) for row in rows]

    def get_course_grades(self, course_id: str) -> list[Grade]:
        """Return all grades for one existing course."""

        self.get_course(course_id)

        rows = self.connection.execute(
            self._grade_select_sql() + " WHERE g.course_id = ? ORDER BY g.id",
            (course_id,),
        ).fetchall()

        return [self._row_to_grade(row) for row in rows]

    # ========================================================
    # Grade CRUD: Update
    # ========================================================

    def update_grade(self, grade_id: int, grade: Grade) -> None:
        """Replace the stored values of an existing grade."""

        self.get_grade(grade_id)
        self.get_student(grade.student.student_id)
        self.get_course(grade.course.course_id)

        try:
            with self.connection:
                self.connection.execute(
                    """
                    UPDATE grades
                    SET student_id = ?, course_id = ?, score = ?, date = ?, notes = ?
                    WHERE id = ?
                    """,
                    (
                        grade.student.student_id,
                        grade.course.course_id,
                        grade.score,
                        grade.date,
                        grade.notes,
                        grade_id,
                    ),
                )
        except sqlite3.Error as error:
            raise PersistenceError("Could not update grade in database.") from error

    # ========================================================
    # Grade CRUD: Delete
    # ========================================================

    def delete_grade(self, grade_id: int) -> None:
        """Delete one grade by its database ID."""

        self.get_grade(grade_id)

        try:
            with self.connection:
                self.connection.execute(
                    "DELETE FROM grades WHERE id = ?",
                    (grade_id,),
                )
        except sqlite3.Error as error:
            raise PersistenceError("Could not delete grade from database.") from error

    # ========================================================
    # SQL Statistics: Student Average
    # ========================================================

    def student_average(self, student_id: str) -> float:
        """Calculate a student's average percentage with SQL AVG and JOIN."""

        self.get_student(student_id)

        row = self.connection.execute(
            """
            SELECT AVG(g.score / c.max_grade * 100.0) AS average_percentage
            FROM grades AS g
            JOIN courses AS c ON g.course_id = c.course_id
            WHERE g.student_id = ?
            """,
            (student_id,),
        ).fetchone()

        if row["average_percentage"] is None:
            raise ValueError(f"No grades recorded for student {student_id}.")

        return float(row["average_percentage"])

    # ========================================================
    # SQL Statistics: Course Average
    # ========================================================

    def course_average(self, course_id: str) -> float:
        """Calculate a course's average score with SQL AVG."""

        self.get_course(course_id)

        row = self.connection.execute(
            """
            SELECT AVG(score) AS average_score
            FROM grades
            WHERE course_id = ?
            """,
            (course_id,),
        ).fetchone()

        if row["average_score"] is None:
            raise ValueError(f"No grades recorded for course {course_id}.")

        return float(row["average_score"])

    # ========================================================
    # SQL Statistics: Course Pass Rate
    # ========================================================

    def course_pass_rate(self, course_id: str) -> float:
        """Calculate a course's pass rate with SQL AVG, CASE, and JOIN."""

        self.get_course(course_id)

        row = self.connection.execute(
            """
            SELECT AVG(
                CASE WHEN g.score >= c.passing_grade THEN 1.0 ELSE 0.0 END
            ) * 100.0 AS pass_rate
            FROM grades AS g
            JOIN courses AS c ON g.course_id = c.course_id
            WHERE g.course_id = ?
            """,
            (course_id,),
        ).fetchone()

        if row["pass_rate"] is None:
            raise ValueError(f"No grades recorded for course {course_id}.")

        return float(row["pass_rate"])

    # ========================================================
    # SQL Statistics: All Student Averages
    # ========================================================

    def student_averages(self) -> list[tuple[str, float]]:
        """Return all student averages using JOIN, AVG, and GROUP BY."""

        rows = self.connection.execute(
            """
            SELECT
                s.student_id,
                AVG(g.score / c.max_grade * 100.0) AS average_percentage
            FROM students AS s
            JOIN grades AS g ON s.student_id = g.student_id
            JOIN courses AS c ON g.course_id = c.course_id
            GROUP BY s.student_id
            ORDER BY average_percentage DESC, s.student_id
            """
        ).fetchall()

        return [
            (row["student_id"], float(row["average_percentage"]))
            for row in rows
        ]

    # ========================================================
    # SQL Statistics: Course Overview
    # ========================================================

    def course_statistics(self) -> list[dict]:
        """Return grade count, average, and pass rate for every course.

        This query demonstrates the required SQL concepts COUNT, AVG,
        GROUP BY, LEFT JOIN, and CASE. Courses without grades are included.
        """

        rows = self.connection.execute(
            """
            SELECT
                c.course_id,
                c.name,
                COUNT(g.id) AS grade_count,
                AVG(g.score) AS average_score,
                AVG(
                    CASE
                        WHEN g.id IS NULL THEN NULL
                        WHEN g.score >= c.passing_grade THEN 1.0
                        ELSE 0.0
                    END
                ) * 100.0 AS pass_rate
            FROM courses AS c
            LEFT JOIN grades AS g ON c.course_id = g.course_id
            GROUP BY c.course_id, c.name
            ORDER BY c.course_id
            """
        ).fetchall()

        return [
            {
                "course_id": row["course_id"],
                "name": row["name"],
                "grade_count": row["grade_count"],
                "average_score": row["average_score"],
                "pass_rate": row["pass_rate"],
            }
            for row in rows
        ]

    # ========================================================
    # Connection Management
    # ========================================================

    def close(self) -> None:
        """Close the SQLite database connection."""

        self.connection.close()

    def __enter__(self) -> "GradeDatabase":
        """Return this database when it is used in a with statement."""

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Close the database after a with statement."""

        self.close()

    # ========================================================
    # Helper Methods: Convert SQL Rows into Domain Objects
    # ========================================================

    @staticmethod
    def _row_to_student(row: sqlite3.Row) -> Student:
        """Convert one SQLite row into a Student object."""

        return Student(
            student_id=row["student_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
        )

    @staticmethod
    def _row_to_course(row: sqlite3.Row) -> Course:
        """Convert one SQLite row into a Course object."""

        return Course(
            course_id=row["course_id"],
            name=row["name"],
            max_grade=row["max_grade"],
            passing_grade=row["passing_grade"],
        )

    @staticmethod
    def _row_to_grade(row: sqlite3.Row) -> Grade:
        """Convert one joined SQLite row into a Grade object."""

        student = Student(
            student_id=row["student_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
        )

        course = Course(
            course_id=row["course_id"],
            name=row["course_name"],
            max_grade=row["max_grade"],
            passing_grade=row["passing_grade"],
        )

        return Grade(
            student=student,
            course=course,
            score=row["score"],
            date=row["date"],
            notes=row["notes"],
        )

    @staticmethod
    def _grade_select_sql() -> str:
        """Return the shared JOIN query used to rebuild Grade objects."""

        return """
        SELECT
            g.id,
            g.score,
            g.date,
            g.notes,
            s.student_id,
            s.first_name,
            s.last_name,
            s.email,
            c.course_id,
            c.name AS course_name,
            c.max_grade,
            c.passing_grade
        FROM grades AS g
        JOIN students AS s ON g.student_id = s.student_id
        JOIN courses AS c ON g.course_id = c.course_id
        """
