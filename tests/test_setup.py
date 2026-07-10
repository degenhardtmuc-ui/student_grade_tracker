"""Basic project setup tests.

This test file checks whether pytest can run correctly
and whether the main project classes and custom exceptions
can be imported without errors.
"""

# ============================================================
# Test: Project Imports and Setup
# ============================================================

def test_project_setup():
    """Test that the project setup and basic imports are working.

    This test checks whether pytest can run correctly and whether
    the main project classes and custom exceptions can be imported
    without errors.

    If one of these imports fails, the project structure or package
    setup probably needs to be checked.
    """

    from notenverwaltung.course import Course
    from notenverwaltung.exceptions import (
        CourseNotFoundError,
        DuplicateEntryError,
        PersistenceError,
        StudentNotFoundError,
    )
    from notenverwaltung.grade import Grade
    from notenverwaltung.gradebook import GradeBook
    from notenverwaltung.student import Student

    assert Course is not None
    assert Grade is not None
    assert GradeBook is not None
    assert Student is not None

    assert CourseNotFoundError is not None
    assert DuplicateEntryError is not None
    assert PersistenceError is not None
    assert StudentNotFoundError is not None