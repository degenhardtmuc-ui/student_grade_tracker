"""Custom exception classes for the GradeBook system.

This module contains all custom exceptions that are used in the
student grade management project.

Custom exceptions make error handling clearer because the program can
raise specific errors instead of using only general Python errors.
"""


# ============================================================
# Student Error: Student ID Does Not Exist
# ============================================================

class StudentNotFoundError(ValueError):
    """Raise this error when a student ID does not exist.

    This exception is used when the program tries to find, update,
    or use a student that is not stored in the GradeBook.

    It inherits from ValueError so that older tests with
    pytest.raises(ValueError) still remain valid.
    """


# ============================================================
# Course Error: Course ID Does Not Exist
# ============================================================

class CourseNotFoundError(ValueError):
    """Raise this error when a course ID does not exist.

    This exception is used when the program tries to find, update,
    or use a course that is not stored in the GradeBook.

    It inherits from ValueError so that older tests with
    pytest.raises(ValueError) still remain valid.
    """


# ============================================================
# Duplicate Error: Student or Course Already Exists
# ============================================================

class DuplicateEntryError(ValueError):
    """Raise this error when a student or course already exists.

    This exception is used when the program tries to add a student
    or a course with an ID that is already stored in the GradeBook.

    It inherits from ValueError so that older tests with
    pytest.raises(ValueError) still remain valid.
    """


# ============================================================
# Persistence Error: Saving or Loading Data Failed
# ============================================================

class PersistenceError(Exception):
    """Raise this error when saving or loading data fails.

    This exception is used for file-related problems, for example:
    missing files, invalid JSON content, broken CSV files, or invalid
    file paths.

    It inherits directly from Exception because persistence errors
    are not simple value errors. They are technical file handling errors.
    """