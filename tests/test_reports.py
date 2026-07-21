"""Tests for the report generator classes."""

import pytest

from notenverwaltung.gradebook import GradeBook
from notenverwaltung.reports.base import ReportGenerator


def test_report_generator_cannot_be_instantiated() -> None:
    """Test that the abstract ReportGenerator cannot be instantiated."""
    gradebook = GradeBook()

    with pytest.raises(TypeError):
        ReportGenerator(gradebook)