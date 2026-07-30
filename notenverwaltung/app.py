"""Gradio user interface for the Student Grade Tracker."""

import sqlite3
from pathlib import Path

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.reports.text_report import TextReportGenerator
from notenverwaltung.student import Student
from notenverwaltung.exceptions import (
    CourseNotFoundError,
    StudentNotFoundError,
)
from notenverwaltung.auth import login_student, register_student

# app.py liegt im Ordner notenverwaltung.
# parent.parent führt deshalb zum Projektordner.
DATABASE_PATH = (
    Path(__file__).resolve().parent.parent / "grade_tracker.db"
)

# Nur diese Tabellennamen dürfen verwendet werden.
ALLOWED_TABLES = {"students", "courses", "grades"}

def get_next_student_id(database_path: Path) -> str:
    """Return the next free student ID in the format S001, S002, ..."""

    if not database_path.exists():
        return "S001"

    with sqlite3.connect(database_path) as connection:
        result = connection.execute(
            """
            SELECT student_id
            FROM students
            WHERE student_id LIKE 'S%'
            ORDER BY CAST(SUBSTR(student_id, 2) AS INTEGER) DESC
            LIMIT 1
            """
        ).fetchone()

    if result is None:
        return "S001"

    last_student_id = result[0]
    next_number = int(last_student_id[1:]) + 1

    return f"S{next_number:03d}"

def welcome(name: str) -> str:
    """Return a short welcome message."""

    return f"Willkommen bei der Notenverwaltung, {name}!"

def register_from_form(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    password_repeat: str,
) -> str:
    """Register a new student with an automatically generated student ID."""

    student_id = get_next_student_id(DATABASE_PATH)

    result = register_student(
        DATABASE_PATH,
        student_id,
        first_name,
        last_name,
        email,
        password,
        password_repeat,
    )

    return f"{result}\n\nStudent-ID: {student_id}"

    return register_student(
        DATABASE_PATH,
        student_id,
        first_name,
        last_name,
        email,
        password,
        password_repeat,
    )


def login_from_form(student_id: str, password: str) -> str:
    """Verbinde das Anmeldeformular mit der Passwortprüfung."""

    return login_student(
        DATABASE_PATH,
        student_id,
        password,
    )

def create_demo_gradebook() -> GradeBook:
    """Create a small demo gradebook for the report tab."""
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
    gradebook.add_course(
        Course("CS102", "Python Programming")
    )

    gradebook.add_course(
        Course("DB101", "Database Fundamentals")
    )

    gradebook.record_grade(
        "S001", "CS102", 92.0, "2026-07-10"
    )
    gradebook.record_grade(
        "S002", "CS102", 76.0, "2026-07-10"
    )
    gradebook.record_grade(
        "S001", "DB101", 88.0, "2026-07-12"
    )
    gradebook.record_grade(
        "S002", "DB101", 67.0, "2026-07-12"
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

def create_database_gradebook() -> GradeBook:
    """Erzeuge ein GradeBook aus den Daten der SQLite-Datenbank."""
    gradebook = GradeBook()

    with sqlite3.connect(DATABASE_PATH) as connection:
        students = connection.execute(
            """
            SELECT student_id, first_name, last_name, email
            FROM students
            ORDER BY student_id
            """
        ).fetchall()

        courses = connection.execute(
            """
            SELECT course_id, name, max_grade, passing_grade
            FROM courses
            ORDER BY course_id
            """
        ).fetchall()

        grades = connection.execute(
            """
            SELECT student_id, course_id, score, date, notes
            FROM grades
            ORDER BY date
            """
        ).fetchall()

    for student_id, first_name, last_name, email in students:
        gradebook.add_student(
            Student(student_id, first_name, last_name, email)
        )

    for course_id, name, max_grade, passing_grade in courses:
        gradebook.add_course(
            Course(course_id, name, max_grade, passing_grade)
        )

    for student_id, course_id, score, date, notes in grades:
        gradebook.record_grade(
            student_id,
            course_id,
            score,
            date,
            notes or "",
        )

    return gradebook

def generate_dashboard() -> str:
    """Generate dashboard values from the SQLite database."""

    if not DATABASE_PATH.exists():
        return f"Datenbank nicht gefunden: {DATABASE_PATH}"

    with sqlite3.connect(DATABASE_PATH) as connection:
        student_count = connection.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        course_count = connection.execute(
            "SELECT COUNT(*) FROM courses"
        ).fetchone()[0]

        grade_count = connection.execute(
            "SELECT COUNT(*) FROM grades"
        ).fetchone()[0]

        statistics = connection.execute(
            """
            SELECT
                COALESCE(AVG(g.score / c.max_grade * 100), 0),
                COALESCE(
                    AVG(
                        CASE
                            WHEN g.score >= c.passing_grade
                            THEN 100.0
                            ELSE 0.0
                        END
                    ),
                    0
                )
            FROM grades AS g
            JOIN courses AS c
                ON g.course_id = c.course_id
            """
        ).fetchone()

    overall_average = statistics[0]
    pass_rate = statistics[1]

    return f"""
| Kennzahl | Aktueller Wert |
|---|---:|
| Studenten | {student_count} |
| Kurse | {course_count} |
| Erfasste Noten | {grade_count} |
| Gesamtdurchschnitt | {overall_average:.1f} % |
| Bestehensquote | {pass_rate:.1f} % |
"""

def generate_pass_chart() -> pd.DataFrame:
    """Generate pass and fail statistics from the SQLite database."""

    if not DATABASE_PATH.exists():
        return pd.DataFrame(
            {
                "Status": [],
                "Anzahl": [],
            }
        )

    with sqlite3.connect(DATABASE_PATH) as connection:
        result = connection.execute(
            """
            SELECT
                SUM(
                    CASE
                        WHEN g.score >= c.passing_grade
                        THEN 1
                        ELSE 0
                    END
                ),
                SUM(
                    CASE
                        WHEN g.score < c.passing_grade
                        THEN 1
                        ELSE 0
                    END
                )
            FROM grades AS g
            JOIN courses AS c
                ON g.course_id = c.course_id
            """
        ).fetchone()

    passed_count = result[0] or 0
    failed_count = result[1] or 0

    return pd.DataFrame(
        {
            "Status": [
                "Bestanden",
                "Nicht bestanden",
            ],
            "Anzahl": [
                passed_count,
                failed_count,
            ],
        }
    )    

def generate_pass_plot():
    """Erzeuge ein Balkendiagramm für bestandene und nicht bestandene Noten."""
    chart_data = generate_pass_chart()

    figure, axis = plt.subplots(figsize=(8, 4))

    axis.bar(
        chart_data["Status"],
        chart_data["Anzahl"],
        color=["#4C78A8", "#F58518"],
    )

    axis.set_title("Bestanden und nicht bestanden")
    axis.set_xlabel("Status")
    axis.set_ylabel("Anzahl der Noten")
    axis.set_ylim(0, max(chart_data["Anzahl"].max() + 1, 2))
    axis.grid(axis="y", alpha=0.25)

    figure.tight_layout()
    return figure

def generate_text_report(report_type: str, identifier: str) -> str:                
    """Generate a text report for the selected  report type."""

    gradebook = create_database_gradebook()
    generator = TextReportGenerator(gradebook)

    try:
        if report_type == "Student":
            return generator.student_report(identifier)

        if report_type == "Course":
            return generator.course_report(identifier)

        if report_type == "Summary":
            return generator.summary_report()

        return "Unknown report type."

    except StudentNotFoundError:
        return f"Student mit ID {identifier} ist nicht immatrikuliert."

    except CourseNotFoundError:
        return f"Course mit ID {identifier} exsistiert nicht."

def generate_selected_report(
    report_type: str,
    student_id: str,
    course_id: str,
) -> str:
    """Select the correct identifier and generate the requested report."""

    if report_type == "Student":
        return generate_text_report("Student", student_id)

    if report_type == "Course":
        return generate_text_report("Course", course_id)

    if report_type == "Summary":
        return generate_text_report("Summary", "")

    return "Unbekannter Report-Typ."

def update_report_inputs(report_type: str):
    """Show only the dropdown required for the selected report type."""

    if report_type == "Student":
        return (
            gr.update(visible=True),
            gr.update(visible=False),
        )

    if report_type == "Course":
        return (
            gr.update(visible=False),
            gr.update(visible=True),
        )

    return (
        gr.update(visible=False),
        gr.update(visible=False),
    )

def load_table(table_name: str) -> pd.DataFrame:
    """Read one permitted table from the SQLite database."""

    if table_name not in ALLOWED_TABLES:
        return pd.DataFrame(
            {"Fehler": ["Diese Tabelle ist nicht erlaubt."]}
        )

    if not DATABASE_PATH.exists():
        return pd.DataFrame(
            {
                "Fehler": [
                    f"Datenbank nicht gefunden: {DATABASE_PATH}"
                ]
            }
        )

    with sqlite3.connect(DATABASE_PATH) as connection:
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql_query(query, connection)
        
def load_student_choices():
    """Lade die Studentenauswahl aus SQLite."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        students = connection.execute(
            """
            SELECT student_id, first_name, last_name
            FROM students
            ORDER BY student_id
            """
        ).fetchall()

    return [
        (f"{student_id} - {first_name} {last_name}", student_id)
        for student_id, first_name, last_name in students
    ]


def load_course_choices():
    """Lade die Kursauswahl aus SQLite."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        courses = connection.execute(
            """
            SELECT course_id, name
            FROM courses
            ORDER BY course_id
            """
        ).fetchall()

    return [
        (f"{course_id} - {name}", course_id)
        for course_id, name in courses
    ]


student_choices = load_student_choices()
course_choices = load_course_choices()

def export_table_to_csv(table_name: str) -> str:
    """Export one permitted SQLite table as a CSV file."""

    if table_name not in ALLOWED_TABLES:
        raise gr.Error("Diese Tabelle darf nicht exportiert werden.")

    if not DATABASE_PATH.exists():
        raise gr.Error(f"Datenbank nicht gefunden: {DATABASE_PATH}")

    export_directory = DATABASE_PATH.parent / "exports"
    export_directory.mkdir(exist_ok=True)

    export_path = export_directory / f"{table_name}.csv"

    with sqlite3.connect(DATABASE_PATH) as connection:
        query = f"SELECT * FROM {table_name}"
        table_data = pd.read_sql_query(query, connection)

    table_data.to_csv(
        export_path,
        index=False,
        encoding="utf-8",
    )

    return str(export_path)

with gr.Blocks(title="Student Grade Tracker") as app:
    gr.Markdown("# Student Grade Tracker")
    gr.Markdown("Notenverwaltung mit Python, SQLite und Gradio")

    with gr.Tab("Dashboard"):
        gr.Markdown("## Dashboard")

        gr.Markdown(
            generate_dashboard()
        )

        gr.Markdown("### Bestehensverteilung")

        gr.Plot(
            value=generate_pass_plot(),
            label="Bestanden und nicht bestanden",
        )
    with gr.Tab("Zugang"):
        gr.Markdown("## Studentenzugang")

        with gr.Row():
            with gr.Column():
                gr.Markdown("### Anmelden")

                login_id_input = gr.Textbox(
                    label="Student-ID"
                )

                login_password_input = gr.Textbox(
                    label="Passwort",
                    type="password",
                )

                login_button = gr.Button(
                    "Anmelden",
                    variant="primary",
                )

                login_output = gr.Textbox(
                    label="Anmeldestatus",
                    interactive=False,
                )

                login_button.click(
                    fn=login_from_form,
                    inputs=[
                        login_id_input,
                        login_password_input,
                    ],
                    outputs=login_output,
                )

            with gr.Column():
                gr.Markdown("### Neu registrieren")
                gr.Markdown("Ihre Student-ID wird automatisch vergeben")

                register_id_input = gr.Textbox(
                    label="Student-ID: automatisch erzeugt "
                )
                register_first_name = gr.Textbox(
                    label="Vorname"
                )
                register_last_name = gr.Textbox(
                    label="Nachname"
                )
                register_email = gr.Textbox(
                    label="E-Mail"
                )
                register_password = gr.Textbox(
                    label="Passwort",
                    type="password",
                )
                register_password_repeat = gr.Textbox(
                    label="Passwort wiederholen",
                    type="password",
                )

                register_button = gr.Button(
                    "Registrieren",
                    variant="primary",
                )

                register_output = gr.Textbox(
                    label="Registrierungsstatus",
                    interactive=False,
                )

                register_button.click(
                    fn=register_from_form,
                    inputs=[
                        register_first_name,
                        register_last_name,
                        register_email,
                        register_password,
                        register_password_repeat,
                ],
                outputs=register_output,
                )

    with gr.Tab("SQLite-Datenbank"):
        table_selection = gr.Dropdown(
            choices=["students", "courses", "grades"],
            value="students",
            label="Tabelle auswählen",
        )

        load_button = gr.Button(
            "Tabelle laden",
            variant="primary",
        )

        database_output = gr.Dataframe(
            label="Datenbankinhalt",
            interactive=False,
        )
        
        export_button = gr.Button(
            "Als CSV exportieren"
        )

        export_output = gr.File(
            label="CSV-Datei herunterladen"
        )
        
        load_button.click(
            fn=load_table,
            inputs=table_selection,
            outputs=database_output,
        )
        
        export_button.click(
            fn=export_table_to_csv,
            inputs=table_selection,
            outputs=export_output,
        )
    
    with gr.Tab("Reports"):
        gr.Markdown("## Text Reports")

        report_type_input = gr.Radio(
            choices=["Student", "Course", "Summary"],
            value="Student",
            label="Report type",
        )

        student_input = gr.Dropdown(
            choices=student_choices,
            value="S001",
            label="Student auswählen",
        )

        course_input = gr.Dropdown(
            choices=course_choices,
            value="CS101",
            label="Kurs auswählen",
        )
        
        report_type_input.change(
            fn=update_report_inputs,
            inputs=report_type_input,
            outputs=[
                student_input,
                course_input,
            ],
        )
        
        report_button = gr.Button("Report erzeugen")

        report_output = gr.Textbox(
            label="Report",
            lines=12,
        )

        report_button.click(
            fn=generate_selected_report,
            inputs=[
                report_type_input,
                student_input,
                course_input,
            ],
            outputs=report_output,
        )

if __name__ == "__main__":
    app.launch()