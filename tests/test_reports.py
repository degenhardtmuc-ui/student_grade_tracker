"""Tests for the report generator classes."""

import pytest

from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.reports.base import ReportGenerator
from notenverwaltung.reports.text_report import TextReportGenerator
from notenverwaltung.student import Student


def create_sample_gradebook() -> GradeBook:
    """Create a small grade book used by the report tests."""
    gradebook = GradeBook()

    gradebook.add_student(
        Student("S001", "Anna", "Schmidt", "anna@example.com")
    )
    gradebook.add_student(
        Student("S002", "Ben", "Meyer", "ben@example.com")
    )

    gradebook.add_course(
        Course("CS101", "Intro to Computer Science")
    )

    gradebook.record_grade(
        "S001",
        "CS101",
        85.0,
        "2026-07-07",
    )
    gradebook.record_grade(
        "S002",
        "CS101",
        40.0,
        "2026-07-08",
    )

    return gradebook


def test_report_generator_cannot_be_instantiated() -> None:
    """Test that the abstract ReportGenerator cannot be instantiated."""
    gradebook = GradeBook()

    with pytest.raises(TypeError):
        ReportGenerator(gradebook)


def test_text_student_report() -> None:
    """Test the text report for one student."""
    gradebook = create_sample_gradebook()
    generator = TextReportGenerator(gradebook)

    report = generator.student_report("S001")

    assert "STUDENT REPORT" in report
    assert "Anna Schmidt" in report
    assert "Intro to Computer Science" in report
    assert "Average: 85.00%" in report


def test_text_course_report() -> None:
    """Test the text report for one course."""
    gradebook = create_sample_gradebook()
    generator = TextReportGenerator(gradebook)

    report = generator.course_report("CS101")

    assert "COURSE REPORT" in report
    assert "Intro to Computer Science" in report
    assert "Anna Schmidt" in report
    assert "Ben Meyer" in report
    assert "Average score: 62.50/100.0" in report
    assert "Pass rate: 50.00%" in report


def test_text_summary_report() -> None:
    """Test the summary report for the complete grade book."""
    gradebook = create_sample_gradebook()
    generator = TextReportGenerator(gradebook)

    report = generator.summary_report()

    assert "GRADE BOOK SUMMARY" in report
    assert "Students: 2" in report
    assert "Courses: 1" in report
    assert "Grades: 2" in report
    assert "Intro to Computer Science" in report