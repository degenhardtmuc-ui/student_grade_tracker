import json
import re
from pathlib import Path

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

# Phase 3A: JSON persistence
    

    def to_dict(self) -> dict:
        """Converts the whole grade book into simple Python data."""
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

    @classmethod
    def from_dict(cls, data: dict) -> "GradeBook":
        """Creates a GradeBook object from simple Python data."""
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

    def save_json(self, file_path: str) -> None:
        """Saves the whole grade book as a JSON file."""
        path = Path(file_path)
        data = self.to_dict()

        json_text = json.dumps(data, indent=4)
        path.write_text(json_text, encoding="utf-8")

    @classmethod
    def load_json(cls, file_path: str) -> "GradeBook":
        """Loads a grade book from a JSON file."""
        path = Path(file_path)
        json_text = path.read_text(encoding="utf-8")

        data = json.loads(json_text)

        return cls.from_dict(data)

    
# Phase 3B: CSV export and import for grades
    

    def export_grades_to_csv(self, file_path: str) -> None:
        """Exports all grades as a simple CSV file."""
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

    def import_grades_from_csv(self, file_path: str) -> dict:
        """Imports grades from a CSV file and returns an import report."""
        path = Path(file_path)
        lines = path.read_text(encoding="utf-8").splitlines()

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