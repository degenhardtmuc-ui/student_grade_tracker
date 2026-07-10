# Project Description: Student Grade Tracker

## Overview

The Student Grade Tracker is a Python project for managing students, courses, grades, and grade statistics.

The goal of the project is to create a simple, structured, and understandable grade management system. The system can store students, store courses, record grades, calculate averages, calculate pass rates, search data, and save or load information from files.

The project is written in Python and uses object-oriented programming. The main idea is to separate the responsibilities into different classes. Each class has a clear task inside the application.

---

## Project Goal

The goal of this project is to build a clean and understandable student grade management system.

The application should be able to manage students, manage courses, record grades, calculate student averages, calculate course averages, calculate course pass rates, find top students, find students at risk, search for students and courses, save the grade book as JSON, load the grade book from JSON, export grades to CSV, import grades from CSV, handle errors with custom exceptions, and verify the behavior with automated tests.

The project also focuses on clean code structure, readable names, validation, docstrings, and tests.

---

## Main Idea

The most important idea of the project is that a grade connects one student with one course.

A student can have many grades. A course can have many grades. Each grade belongs to one student and one course.

The GradeBook is the central class of the project. It manages all students, all courses, and all recorded grades.

In simple words:

```text
Student + Course + Score = Grade
GradeBook manages everything.
```

---

## Project Structure

The project is organized into separate files and folders.

Example structure:

```text
student_grade_tracker/
│
├── notenverwaltung/
│   ├── __init__.py
│   ├── student.py
│   ├── course.py
│   ├── grade.py
│   ├── gradebook.py
│   └── exceptions.py
│
├── tests/
│   ├── __init__.py
│   ├── test_setup.py
│   ├── test_student.py
│   ├── test_course.py
│   ├── test_grade.py
│   ├── test_gradebook.py
│   ├── test_exceptions.py
│   └── test_persistence.py
│
├── docs/
│   ├── domain_model.md
│   └── projektbeschreibung.md
│
└── README.md
```

The `notenverwaltung` folder contains the actual application code.

The `tests` folder contains the automated tests.

The `docs` folder contains project documentation, such as the domain model and the project description.

---

## Main Classes

The project contains four main domain classes:

- `Student`
- `Course`
- `Grade`
- `GradeBook`

It also contains custom exception classes for special error situations.

---

## Student Class

The `Student` class represents one student in the grade tracker.

A student has a student ID, a first name, a last name, and an email address.

The class also provides a `full_name` property. This property combines the first name and the last name into one readable full name.

The responsibility of the `Student` class is to store student information and validate basic student data.

Important validation rules:

- The student ID must not be empty.
- The first name must not be empty.
- The last name must not be empty.
- The email address must contain `@`.

Example:

```text
student_id: S001
first_name: Anna
last_name: Schmidt
email: anna@example.com
```

---

## Course Class

The `Course` class represents one subject or course.

A course has a course ID, a course name, a maximum possible grade, and a passing grade.

The responsibility of the `Course` class is to store course information and define the grade limits for that course.

Important validation rules:

- The course ID must not be empty.
- The course name must not be empty.
- The maximum grade must be greater than zero.
- The passing grade must be greater than zero.
- The passing grade must not be greater than the maximum grade.

Example:

```text
course_id: CS101
name: Intro to Computer Science
max_grade: 100.0
passing_grade: 50.0
```

---

## Grade Class

The `Grade` class represents one recorded grade.

A grade connects one student with one course. It also stores the achieved score, the date, and optional notes.

The class provides calculated properties:

- `is_passing`
- `percentage`
- `letter_grade`

The responsibility of the `Grade` class is to store one grade and calculate useful information from it.

Important validation rules:

- The score must not be below zero.
- The score must not be higher than the maximum grade of the course.
- The date must use ISO format.

Example:

```text
student: Anna Schmidt
course: Intro to Computer Science
score: 85.0
date: 2026-07-07
```

---

## GradeBook Class

The `GradeBook` class is the central management class of the project.

It stores all students, all courses, and all grades.

The `GradeBook` is responsible for connecting the other classes and providing the main functionality of the application.

The class can add students, add courses, record grades, get grades by student, get grades by course, calculate averages, calculate pass rates, find top students, find students at risk, search students, search courses, save data as JSON, load data from JSON, export grades to CSV, and import grades from CSV.

The `GradeBook` therefore works like the central control unit of the whole application.

---

## Custom Exceptions

The project uses custom exceptions to make error messages clearer.

The custom exceptions are:

- `StudentNotFoundError`
- `CourseNotFoundError`
- `DuplicateEntryError`
- `PersistenceError`

These custom exceptions make the program easier to understand because each error has a clear meaning.

For example:

```text
StudentNotFoundError means that a student ID does not exist.
CourseNotFoundError means that a course ID does not exist.
DuplicateEntryError means that a student or course already exists.
PersistenceError means that saving or loading data failed.
```

The first three custom exceptions inherit from `ValueError`. This keeps older tests with `pytest.raises(ValueError)` valid while still making the error types more specific.

---

## Persistence

Persistence means that data can be saved and loaded again.

This project supports two forms of persistence:

- JSON
- CSV

JSON is used to save and load the complete grade book.

CSV is used to export and import grade data.

---

## JSON Saving and Loading

JSON is used to save and load the complete `GradeBook`.

The `GradeBook` can be converted into simple dictionary data. This dictionary data can then be saved as JSON.

Important methods:

- `to_dict()`
- `from_dict(data)`
- `save_json(file_path)`
- `load_json(file_path)`

JSON is useful because it can store the complete structure of the grade book.

It can store:

- students
- courses
- grades

This makes it possible to save the current state of the application and load it again later.

---

## CSV Export and Import

CSV is used for grade data.

The project can export all recorded grades into a CSV file.

Example CSV format:

```text
student_id,course_id,score,date
S001,CS101,85.0,2026-07-07
S002,CS101,45.0,2026-07-07
```

The project can also import grades from a CSV file.

During import, valid lines are imported and invalid lines are skipped. The import method returns a report that shows how many lines were imported, how many lines were skipped, and which errors occurred.

This makes the CSV import safer and easier to check.

---

## Search Functions

The project includes search functions for students and courses.

Students can be searched by first name, last name, email, or full name.

Courses can be searched by course name.

The search uses regular expressions and is case-insensitive. This means that uppercase and lowercase letters do not matter.

Example:

```text
Searching for "anna" can find "Anna Schmidt".
Searching for "data" can find "Data Structures".
```

---

## Statistics

The project can calculate different statistics.

The `GradeBook` can calculate the average percentage of one student, the average score of one course, the pass rate of one course, the top students, and students below a risk threshold.

These statistics help to understand the performance of students and courses.

Examples:

```text
Student average: Shows the average result of one student.
Course average: Shows the average score in one course.
Course pass rate: Shows how many students passed a course.
Top students: Shows the students with the best averages.
Students at risk: Shows students below a defined threshold.
```

---

## Testing

The project uses `pytest` for automated testing.

The tests check whether the application behaves correctly.

The test files cover student creation and validation, course creation and validation, grade creation and validation, grade calculations, grade book management, duplicate entries, unknown students, unknown courses, JSON saving and loading, CSV export and import, custom exceptions, and basic project setup.

Automated tests are important because they make the project more reliable.

If a future change breaks existing behavior, pytest can detect the problem.

---

## Example Workflow

A typical workflow in the project looks like this:

```text
1. Create a GradeBook.
2. Add students.
3. Add courses.
4. Record grades.
5. Calculate averages and pass rates.
6. Search for students or courses.
7. Save the GradeBook as JSON.
8. Export grades as CSV.
```

Example:

```text
Student: Anna Schmidt
Course: Intro to Computer Science
Score: 85.0
Date: 2026-07-07
Result: Passed
```

---

## Technologies Used

The project uses:

- Python
- dataclasses
- pytest
- JSON
- CSV
- regular expressions
- pathlib
- custom exceptions
- object-oriented programming

---

## Object-Oriented Programming

The project uses object-oriented programming to keep the code organized.

Each class has a clear responsibility.

| Class | Responsibility |
|---|---|
| `Student` | Stores student data |
| `Course` | Stores course data and grade limits |
| `Grade` | Connects one student with one course and stores a score |
| `GradeBook` | Manages students, courses, grades, statistics, and file operations |
| `StudentNotFoundError` | Represents a missing student |
| `CourseNotFoundError` | Represents a missing course |
| `DuplicateEntryError` | Represents duplicate students or courses |
| `PersistenceError` | Represents saving or loading problems |

This structure makes the project easier to read, test, and extend.

---

## Validation

Validation is an important part of the project.

The project checks data early to avoid invalid objects.

Examples:

```text
A student cannot have an empty student ID.
A course cannot have a passing grade above the maximum grade.
A grade cannot have a score higher than the course maximum grade.
A grade date must use ISO format.
```

This makes the project safer and reduces unexpected errors.

---

## Error Handling

The project uses exceptions to handle error situations.

Examples of error situations are adding the same student twice, adding the same course twice, recording a grade for an unknown student, recording a grade for an unknown course, loading a missing JSON file, loading invalid JSON data, or importing a missing CSV file.

Instead of silently ignoring these problems, the project raises clear errors.

This makes debugging easier.

---

## Why This Project Is Useful

The Student Grade Tracker is useful because it combines several important programming concepts in one project.

It includes classes, objects, dataclasses, properties, validation, lists, dictionaries, file handling, JSON, CSV, exceptions, and tests.

The project is small enough to understand, but large enough to practice real software structure.

It shows how different parts of a program can work together in a clean and organized way.

---

## Possible Future Improvements

The project could be extended in the future.

Possible improvements:

- add a command-line interface
- add a graphical user interface
- add more detailed email validation
- support more CSV columns
- add grade categories
- add weighted averages
- add student groups
- add course descriptions
- add more detailed reports
- save and load notes in CSV
- improve date handling
- add more tests for edge cases

These improvements are not required for the current version, but they show how the project could grow.

---

## Short Summary

The Student Grade Tracker is a Python project for managing students, courses, and grades.

The main class is `GradeBook`.

The main idea is:

```text
A Grade connects one Student with one Course.
The GradeBook manages the complete system.
```

The project demonstrates object-oriented programming, validation, custom exceptions, JSON persistence, CSV import/export, and automated testing with pytest.