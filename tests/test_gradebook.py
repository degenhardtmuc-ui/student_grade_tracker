"""Tests for the GradeBook class.

This test file checks the main behavior of the GradeBook system.

The tests cover:
- adding students
- adding courses
- preventing duplicate students and courses
- recording grades
- handling unknown students or courses
- getting grades by student or course
- calculating student averages
- calculating course averages
- calculating course pass rates
- finding top students
- finding students at risk
- searching students and courses
- handling students or courses without grades
- protecting the internal grade list
"""

# ============================================================
# Imports
# ============================================================

import pytest

from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.student import Student


# ============================================================
# Fixture: Reusable GradeBook with Sample Data
# ============================================================

@pytest.fixture
def sample_gradebook():
    """Create a reusable GradeBook object for tests.

    This fixture creates a GradeBook with:
    - three students
    - two courses
    - four recorded grades

    It avoids repeated setup code in the test functions.
    Pytest automatically provides this GradeBook to every test
    function that uses the sample_gradebook parameter.
    """

    gradebook = GradeBook()

    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))
    gradebook.add_student(Student("S002", "Ben", "Mueller", "ben@example.com"))
    gradebook.add_student(Student("S003", "Clara", "Weber", "clara@example.com"))

    gradebook.add_course(Course("CS101", "Intro to Computer Science"))
    gradebook.add_course(Course("CS102", "Data Structures"))

    gradebook.record_grade("S001", "CS101", 85.0, "2026-07-07")
    gradebook.record_grade("S001", "CS102", 95.0, "2026-07-08")
    gradebook.record_grade("S002", "CS101", 45.0, "2026-07-07")
    gradebook.record_grade("S003", "CS101", 70.0, "2026-07-07")

    return gradebook


# ============================================================
# Test: Add Student
# ============================================================

def test_add_student():
    """Test that a student can be added to the GradeBook.

    This test creates an empty GradeBook, adds one student,
    and checks whether the student is stored under the correct ID.
    """

    gradebook = GradeBook()
    student = Student("S001", "Anna", "Schmidt", "anna@example.com")

    gradebook.add_student(student)

    assert gradebook.students["S001"] == student


# ============================================================
# Test: Prevent Duplicate Students
# ============================================================

def test_add_duplicate_student_raises_value_error():
    """Test that duplicate student IDs are not allowed.

    The GradeBook should not allow two students with the same student ID.
    This test adds one student and then tries to add the same student again.

    The second attempt must raise ValueError.
    """

    gradebook = GradeBook()
    student = Student("S001", "Anna", "Schmidt", "anna@example.com")

    gradebook.add_student(student)

    with pytest.raises(ValueError):
        gradebook.add_student(student)


# ============================================================
# Test: Add Course
# ============================================================

def test_add_course():
    """Test that a course can be added to the GradeBook.

    This test creates an empty GradeBook, adds one course,
    and checks whether the course is stored under the correct ID.
    """

    gradebook = GradeBook()
    course = Course("CS101", "Intro to Computer Science")

    gradebook.add_course(course)

    assert gradebook.courses["CS101"] == course


# ============================================================
# Test: Prevent Duplicate Courses
# ============================================================

def test_add_duplicate_course_raises_value_error():
    """Test that duplicate course IDs are not allowed.

    The GradeBook should not allow two courses with the same course ID.
    This test adds one course and then tries to add the same course again.

    The second attempt must raise ValueError.
    """

    gradebook = GradeBook()
    course = Course("CS101", "Intro to Computer Science")

    gradebook.add_course(course)

    with pytest.raises(ValueError):
        gradebook.add_course(course)


# ============================================================
# Test: Record Grade
# ============================================================

def test_record_grade(sample_gradebook):
    """Test that record_grade creates and stores a Grade object.

    This test records a new grade for an existing student and course.
    It checks whether the created grade contains the correct student,
    course, score, and whether it is stored inside the GradeBook.
    """

    grade = sample_gradebook.record_grade("S001", "CS101", 90.0, "2026-07-09")

    assert grade.student.student_id == "S001"
    assert grade.course.course_id == "CS101"
    assert grade.score == 90.0
    assert grade in sample_gradebook.grades


# ============================================================
# Test: Record Grade with Unknown Student
# ============================================================

def test_record_grade_unknown_student_raises_value_error(sample_gradebook):
    """Test that a grade cannot be recorded for an unknown student.

    A grade can only be recorded if the student already exists
    in the GradeBook.

    This test uses a student ID that does not exist and expects ValueError.
    """

    with pytest.raises(ValueError):
        sample_gradebook.record_grade("S999", "CS101", 80.0, "2026-07-07")


# ============================================================
# Test: Record Grade with Unknown Course
# ============================================================

def test_record_grade_unknown_course_raises_value_error(sample_gradebook):
    """Test that a grade cannot be recorded for an unknown course.

    A grade can only be recorded if the course already exists
    in the GradeBook.

    This test uses a course ID that does not exist and expects ValueError.
    """

    with pytest.raises(ValueError):
        sample_gradebook.record_grade("S001", "CS999", 80.0, "2026-07-07")


# ============================================================
# Test: Get Grades by Student
# ============================================================

def test_get_student_grades(sample_gradebook):
    """Test that only grades for one selected student are returned.

    This test gets all grades for student S001.
    The sample GradeBook contains exactly two grades for this student.
    """

    grades = sample_gradebook.get_student_grades("S001")

    assert len(grades) == 2
    assert all(grade.student.student_id == "S001" for grade in grades)


# ============================================================
# Test: Get Grades by Course
# ============================================================

def test_get_course_grades(sample_gradebook):
    """Test that only grades for one selected course are returned.

    This test gets all grades for course CS101.
    The sample GradeBook contains exactly three grades for this course.
    """

    grades = sample_gradebook.get_course_grades("CS101")

    assert len(grades) == 3
    assert all(grade.course.course_id == "CS101" for grade in grades)


# ============================================================
# Test: Calculate Student Average
# ============================================================

def test_student_average(sample_gradebook):
    """Test the average percentage for one student.

    Student S001 has two grades:
    - 85.0 percent
    - 95.0 percent

    The expected average is 90.0 percent.
    """

    average = sample_gradebook.student_average("S001")

    assert average == pytest.approx(90.0)


# ============================================================
# Test: Calculate Course Average
# ============================================================

def test_course_average(sample_gradebook):
    """Test the average score for one course.

    Course CS101 has three scores:
    - 85.0
    - 45.0
    - 70.0

    The expected average is approximately 66.67.
    """

    average = sample_gradebook.course_average("CS101")

    assert average == pytest.approx(66.6666667)


# ============================================================
# Test: Calculate Course Pass Rate
# ============================================================

def test_course_pass_rate(sample_gradebook):
    """Test the percentage of passing grades for one course.

    Course CS101 has three grades.
    Two of them are passing grades and one is failing.

    The expected pass rate is approximately 66.67 percent.
    """

    pass_rate = sample_gradebook.course_pass_rate("CS101")

    assert pass_rate == pytest.approx(66.6666667)


# ============================================================
# Test: Find Top Students
# ============================================================

def test_top_students(sample_gradebook):
    """Test that the best students are returned first.

    This test asks for the two best students.
    Student S001 should be first because this student has
    the highest average in the sample GradeBook.
    """

    top_students = sample_gradebook.top_students(n=2)

    assert len(top_students) == 2
    assert top_students[0][0].student_id == "S001"
    assert top_students[0][1] == pytest.approx(90.0)


# ============================================================
# Test: Find Students at Risk
# ============================================================

def test_students_at_risk(sample_gradebook):
    """Test that students below the threshold are returned.

    Students at risk are students whose average is below the given
    threshold.

    In the sample GradeBook, student S002 has an average below 60.0.
    """

    at_risk = sample_gradebook.students_at_risk(threshold=60.0)

    assert len(at_risk) == 1
    assert at_risk[0].student_id == "S002"


# ============================================================
# Test: Search Students by Name
# ============================================================

def test_search_students_by_name(sample_gradebook):
    """Test regex search for students by name.

    The search should be case-insensitive.
    Searching for 'anna' should find student Anna Schmidt.
    """

    result = sample_gradebook.search_students("anna")

    assert len(result) == 1
    assert result[0].student_id == "S001"


# ============================================================
# Test: Search Students by Email
# ============================================================

def test_search_students_by_email(sample_gradebook):
    """Test regex search for students by email.

    Searching for part of Clara's email address should return
    exactly one matching student.
    """

    result = sample_gradebook.search_students("clara@example")

    assert len(result) == 1
    assert result[0].student_id == "S003"


# ============================================================
# Test: Search Courses
# ============================================================

def test_search_courses(sample_gradebook):
    """Test regex search for courses by course name.

    Searching for 'data' should find the course Data Structures.
    The search should be case-insensitive.
    """

    result = sample_gradebook.search_courses("data")

    assert len(result) == 1
    assert result[0].course_id == "CS102"


# ============================================================
# Test: Student Average Without Grades
# ============================================================

def test_no_grades_for_student_raises_value_error():
    """Test that student average calculation fails without grades.

    This test adds a student but does not record any grades for that student.
    Calculating an average without grades is not possible and should
    raise ValueError.
    """

    gradebook = GradeBook()
    gradebook.add_student(Student("S001", "Anna", "Schmidt", "anna@example.com"))

    with pytest.raises(ValueError):
        gradebook.student_average("S001")


# ============================================================
# Test: Course Average Without Grades
# ============================================================

def test_no_grades_for_course_raises_value_error():
    """Test that course average calculation fails without grades.

    This test adds a course but does not record any grades for that course.
    Calculating an average without grades is not possible and should
    raise ValueError.
    """

    gradebook = GradeBook()
    gradebook.add_course(Course("CS101", "Intro to Computer Science"))

    with pytest.raises(ValueError):
        gradebook.course_average("CS101")


# ============================================================
# Test: Returned Grade List Does Not Modify Internal List
# ============================================================

def test_returned_student_grades_do_not_change_internal_list(sample_gradebook):
    """Test that modifying the returned list does not change the GradeBook.

    The get_student_grades method returns a separate list with matching
    grades. If this returned list is modified, the internal grade list
    inside the GradeBook should stay unchanged.

    This protects the original GradeBook data from accidental changes.
    """

    grades = sample_gradebook.get_student_grades("S001")
    grades.clear()

    assert len(sample_gradebook.get_student_grades("S001")) == 2
    assert len(sample_gradebook.grades) == 4