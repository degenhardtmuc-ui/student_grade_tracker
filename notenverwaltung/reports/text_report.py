"""Text report generator for the Student Grade Tracker."""

from notenverwaltung.reports.base import ReportGenerator


class TextReportGenerator(ReportGenerator):
    """Generate readable text reports."""

    def student_report(self, student_id: str) -> str:
        """Generate a text report for one student."""
        grades = self.gradebook.get_student_grades(student_id)
        student = self.gradebook.students[student_id]

        lines = [
            "STUDENT REPORT",
            f"Student: {student.full_name}",
            f"Student ID: {student.student_id}",
            f"Email: {student.email}",
        ]

        if not grades:
            lines.append("No grades recorded.")
            return "\n".join(lines)

        lines.append("Grades:")

        for grade in grades:
            status = "Passed" if grade.is_passing else "Failed"

            lines.append(
                f"- {grade.course.name}: "
                f"{grade.score}/{grade.course.max_grade} "
                f"({grade.percentage:.2f}%, "
                f"{grade.letter_grade}, {status})"
            )

        average = self.gradebook.student_average(student_id)
        lines.append(f"Average: {average:.2f}%")

        return "\n".join(lines)

    def course_report(self, course_id: str) -> str:
        """Generate a text report for one course."""
        grades = self.gradebook.get_course_grades(course_id)
        course = self.gradebook.courses[course_id]

        lines = [
            "COURSE REPORT",
            f"Course: {course.name}",
            f"Course ID: {course.course_id}",
        ]

        if not grades:
            lines.append("No grades recorded.")
            return "\n".join(lines)

        lines.append("Grades:")

        for grade in grades:
            status = "Passed" if grade.is_passing else "Failed"

            lines.append(
                f"- {grade.student.full_name}: "
                f"{grade.score}/{course.max_grade} "
                f"({grade.percentage:.2f}%, "
                f"{grade.letter_grade}, {status})"
            )

        average = self.gradebook.course_average(course_id)
        pass_rate = self.gradebook.course_pass_rate(course_id)

        lines.append(
            f"Average score: {average:.2f}/{course.max_grade}"
        )
        lines.append(f"Pass rate: {pass_rate:.2f}%")

        return "\n".join(lines)

    def summary_report(self) -> str:
        """Generate a summary report for the complete grade book."""
        lines = [
            "GRADE BOOK SUMMARY",
            f"Students: {len(self.gradebook.students)}",
            f"Courses: {len(self.gradebook.courses)}",
            f"Grades: {len(self.gradebook.grades)}",
        ]

        if not self.gradebook.grades:
            lines.append("No grades recorded.")
            return "\n".join(lines)

        lines.append("Course statistics:")

        for course_id, course in self.gradebook.courses.items():
            grades = self.gradebook.get_course_grades(course_id)

            if not grades:
                lines.append(
                    f"- {course.name}: No grades recorded."
                )
                continue

            average = self.gradebook.course_average(course_id)
            pass_rate = self.gradebook.course_pass_rate(course_id)

            lines.append(
                f"- {course.name}: average {average:.2f}/"
                f"{course.max_grade}, "
                f"pass rate {pass_rate:.2f}%"
            )

        return "\n".join(lines)