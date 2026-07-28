"""Gradio user interface for the Student Grade Tracker."""

import sqlite3
from pathlib import Path

import gradio as gr
import pandas as pd
from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.reports.text_report import TextReportGenerator
from notenverwaltung.student import Student
from notenverwaltung.exceptions import (
    CourseNotFoundError,
    StudentNotFoundError,
)

# app.py liegt im Ordner notenverwaltung.
# parent.parent führt deshalb zum Projektordner.
DATABASE_PATH = (
    Path(__file__).resolve().parent.parent / "grade_tracker.db"
)

# Nur diese Tabellennamen dürfen verwendet werden.
ALLOWED_TABLES = {"students", "courses", "grades"}


def welcome(name: str) -> str:
    """Return a short welcome message."""

    return f"Willkommen bei der Notenverwaltung, {name}!"

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

def generate_text_report(report_type: str, identifier: str) -> str:
    """Generate a text report for the selected report type."""

    gradebook = create_demo_gradebook()
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
        
student_choices = [
    ("S001 - Anna Schmidt", "S001"),
    ("S002 - Daniel Degenhardt", "S002"),
]

course_choices = [
    ("CS101 - Intro to Computer Science", "CS101"),
]

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
        gr.Markdown(generate_dashboard())

        gr.Markdown("### Bestehensverteilung")

        gr.BarPlot(
            value=generate_pass_chart(),
            x="Status",
            y="Anzahl",
            color="Status",
            title="Bestanden und nicht bestanden",
            x_title="Status",
            y_title="Anzahl der Noten",
            y_lim=[0, 2],
            height=400,
        )
        
    with gr.Tab("Begrüßung"):
        name_input = gr.Textbox(label="Name")
        welcome_button = gr.Button(
            "Begrüßen",
            variant="primary",
        )
        welcome_output = gr.Textbox(label="Ausgabe")

        welcome_button.click(
            fn=welcome,
            inputs=name_input,
            outputs=welcome_output,
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