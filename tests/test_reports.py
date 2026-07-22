"""Tests for the report generator classes."""

import csv
from io import StringIO

import pytest

from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.reports.base import ReportGenerator
from notenverwaltung.reports.csv_report import CsvReportGenerator
from notenverwaltung.reports.text_report import TextReportGenerator
from notenverwaltung.student import Student

def read_csv_rows(report: str) -> list[dict[str, str]]:
    """Read generated CSV text as dictionaries."""
    return list(csv.DictReader(StringIO(report)))

def create_sample_gradebook() -> GradeBook:
    """Create a small grade book used by the report tests."""
    gradebook = GradeBook()

    gradebook.add_student(
        Student("S001", "Anna", "Schmidt", "anna@example.com")
    )
    gradebook.add_student(
        Student("S002", "Daniel", "Degenhardt", "daniel@example.com")
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
    assert "Daniel Degenhardt" in report
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

def test_csv_student_report() -> None:
    """Test the CSV report for one student."""
    gradebook = create_sample_gradebook()
    generator = CsvReportGenerator(gradebook)

    rows = read_csv_rows(generator.student_report("S001"))

    assert len(rows) == 1
    assert rows[0]["student_id"] == "S001"
    assert rows[0]["student_name"] == "Anna Schmidt"
    assert rows[0]["course_name"] == "Intro to Computer Science"
    assert rows[0]["percentage"] == "85.00"
    assert rows[0]["status"] == "Passed"


def test_csv_course_report() -> None:
    """Test the CSV report for one course."""
    gradebook = create_sample_gradebook()
    generator = CsvReportGenerator(gradebook)

    rows = read_csv_rows(generator.course_report("CS101"))

    assert len(rows) == 2
    assert rows[0]["student_name"] == "Anna Schmidt"
    assert rows[1]["student_name"] == "Daniel Degenhardt"
    assert rows[0]["status"] == "Passed"
    assert rows[1]["status"] == "Failed"


def test_csv_summary_report() -> None:
    """Test the CSV summary for the complete grade book."""
    gradebook = create_sample_gradebook()
    generator = CsvReportGenerator(gradebook)

    rows = read_csv_rows(generator.summary_report())

    assert len(rows) == 1
    assert rows[0]["course_id"] == "CS101"
    assert rows[0]["grade_count"] == "2"
    assert rows[0]["average_score"] == "62.50"
    assert rows[0]["pass_rate"] == "50.00"