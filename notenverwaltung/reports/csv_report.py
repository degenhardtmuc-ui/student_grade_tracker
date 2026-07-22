"""CSV report generator for the Student Grade Tracker."""

import csv
from io import StringIO

from notenverwaltung.reports.base import ReportGenerator


class CsvReportGenerator(ReportGenerator):
    """Generate reports in CSV format."""

    @staticmethod
    def _create_csv(
        headers: list[str],
        rows: list[list[object]],
    ) -> str:
        """Convert headers and rows into one CSV string."""
        output = StringIO()

        writer = csv.writer(
            output,
            lineterminator="\n",
        )

        writer.writerow(headers)
        writer.writerows(rows)

        return output.getvalue()

    def student_report(self, student_id: str) -> str:
        """Generate one CSV row for every grade of a student."""
        student = self.gradebook.students[student_id]
        grades = self.gradebook.get_student_grades(student_id)

        headers = [
            "student_id",
            "student_name",
            "email",
            "course_id",
            "course_name",
            "score",
            "max_grade",
            "percentage",
            "letter_grade",
            "status",
            "date",
            "notes",
        ]

        rows = []

        for grade in grades:
            status = "Passed" if grade.is_passing else "Failed"

            rows.append(
                [
                    student.student_id,
                    student.full_name,
                    student.email,
                    grade.course.course_id,
                    grade.course.name,
                    grade.score,
                    grade.course.max_grade,
                    f"{grade.percentage:.2f}",
                    grade.letter_grade,
                    status,
                    grade.date,
                    grade.notes,
                ]
            )

        return self._create_csv(headers, rows)

    def course_report(self, course_id: str) -> str:
        """Generate one CSV row for every grade in a course."""
        course = self.gradebook.courses[course_id]
        grades = self.gradebook.get_course_grades(course_id)

        headers = [
            "course_id",
            "course_name",
            "student_id",
            "student_name",
            "score",
            "max_grade",
            "percentage",
            "letter_grade",
            "status",
            "date",
            "notes",
        ]

        rows = []

        for grade in grades:
            status = "Passed" if grade.is_passing else "Failed"

            rows.append(
                [
                    course.course_id,
                    course.name,
                    grade.student.student_id,
                    grade.student.full_name,
                    grade.score,
                    course.max_grade,
                    f"{grade.percentage:.2f}",
                    grade.letter_grade,
                    status,
                    grade.date,
                    grade.notes,
                ]
            )

        return self._create_csv(headers, rows)

    def summary_report(self) -> str:
        """Generate one summary CSV row for every course."""
        headers = [
            "course_id",
            "course_name",
            "grade_count",
            "average_score",
            "max_grade",
            "pass_rate",
        ]

        rows = []

        for course_id, course in self.gradebook.courses.items():
            grades = self.gradebook.get_course_grades(course_id)

            if grades:
                average = (
                    f"{self.gradebook.course_average(course_id):.2f}"
                )
                pass_rate = (
                    f"{self.gradebook.course_pass_rate(course_id):.2f}"
                )
            else:
                average = ""
                pass_rate = ""

            rows.append(
                [
                    course.course_id,
                    course.name,
                    len(grades),
                    average,
                    course.max_grade,
                    pass_rate,
                ]
            )

        return self._create_csv(headers, rows)