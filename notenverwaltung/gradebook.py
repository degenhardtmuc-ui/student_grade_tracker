import re

from notenverwaltung.course import Course
from notenverwaltung.grade import Grade
from notenverwaltung.student import Student


class GradeBook:
    """Manages students, courses, grades and grade statistics."""

    def __init__(self) -> None:
        """Creates an empty grade book."""
        self.students: dict[str, Student] = {}
        self.courses: dict[str, Course] = {}
        self.grades: list[Grade] = []

    def add_student(self, student: Student) -> None:
        """Adds one student to the grade book."""
        if student.student_id in self.students:
            raise ValueError(f"Student with ID {student.student_id} already exists.")

        self.students[student.student_id] = student

    def add_course(self, course: Course) -> None:
        """Adds one course to the grade book."""
        if course.course_id in self.courses:
            raise ValueError(f"Course with ID {course.course_id} already exists.")

        self.courses[course.course_id] = course

    def record_grade(
        self,
        student_id: str,
        course_id: str,
        score: float,
        date: str,
        notes: str = "",
    ) -> Grade:
        """Creates and stores one grade for an existing student and course."""
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} does not exist.")

        if course_id not in self.courses:
            raise ValueError(f"Course with ID {course_id} does not exist.")

        student = self.students[student_id]
        course = self.courses[course_id]

        grade = Grade(
            student=student,
            course=course,
            score=score,
            date=date,
            notes=notes,
        )

        self.grades.append(grade)

        return grade

    def get_student_grades(self, student_id: str) -> list[Grade]:
        """Returns all grades for one student."""
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} does not exist.")

        return [grade for grade in self.grades if grade.student.student_id == student_id]

    def get_course_grades(self, course_id: str) -> list[Grade]:
        """Returns all grades for one course."""
        if course_id not in self.courses:
            raise ValueError(f"Course with ID {course_id} does not exist.")

        return [grade for grade in self.grades if grade.course.course_id == course_id]

    def student_average(self, student_id: str) -> float:
        """Returns the average percentage for one student."""
        grades = self.get_student_grades(student_id)

        if not grades:
            raise ValueError(f"No grades recorded for student {student_id}.")

        total_percentage = sum(grade.percentage for grade in grades)

        return total_percentage / len(grades)

    def course_average(self, course_id: str) -> float:
        """Returns the average score for one course."""
        grades = self.get_course_grades(course_id)

        if not grades:
            raise ValueError(f"No grades recorded for course {course_id}.")

        total_score = sum(grade.score for grade in grades)

        return total_score / len(grades)

    def course_pass_rate(self, course_id: str) -> float:
        """Returns the percentage of passing grades for one course."""
        grades = self.get_course_grades(course_id)

        if not grades:
            raise ValueError(f"No grades recorded for course {course_id}.")

        passing_grades = 0

        for grade in grades:
            if grade.is_passing:
                passing_grades = passing_grades + 1

        return passing_grades / len(grades) * 100

    def top_students(self, n: int = 5) -> list[tuple[Student, float]]:
        """Returns the top N students by average percentage."""
        averages = []

        for student_id, student in self.students.items():
            student_grades = self.get_student_grades(student_id)

            if student_grades:
                average = self.student_average(student_id)
                averages.append((student, average))

        averages.sort(key=lambda item: item[1], reverse=True)

        return averages[:n]

    def students_at_risk(self, threshold: float = 60.0) -> list[Student]:
        """Returns students whose average percentage is below the threshold."""
        at_risk_students = []

        for student_id, student in self.students.items():
            student_grades = self.get_student_grades(student_id)

            if student_grades:
                average = self.student_average(student_id)

                if average < threshold:
                    at_risk_students.append(student)

        return at_risk_students

    def search_students(self, query: str) -> list[Student]:
        """Searches students by first name, last name or email using regex."""
        pattern = re.compile(query, re.IGNORECASE)

        return [
            student
            for student in self.students.values()
            if pattern.search(student.first_name)
            or pattern.search(student.last_name)
            or pattern.search(student.email)
            or pattern.search(student.full_name)
        ]

    def search_courses(self, query: str) -> list[Course]:
        """Searches courses by course name using regex."""
        pattern = re.compile(query, re.IGNORECASE)

        return [
            course
            for course in self.courses.values()
            if pattern.search(course.name)
        ]