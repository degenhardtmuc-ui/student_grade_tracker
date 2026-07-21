"""Abstract base class for grade reports"""

from abc import ABC, abstractmethod

from notenverwaltung.gradebook import GradeBook


class ReportGenerator(ABC):
    """Define the common interface for all report generators"""

    def __init__(self, gradebook: GradeBook) -> None:
        """Store the GradeBook used to create reports"""
        self.gradebook = gradebook

    @abstractmethod
    def student_report(self, student_id: str) -> str:
        """Generate a report for one student"""

    @abstractmethod
    def course_report(self, course_id: str) -> str:
        """Generate a report for one course"""

    @abstractmethod
    def summary_report(self) -> str:
        """Generate a summary report for the complete grade book"""