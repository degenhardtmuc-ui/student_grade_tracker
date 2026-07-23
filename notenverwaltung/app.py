"""Gradio user interface for the Student Grade Tracker."""

import sqlite3
from pathlib import Path

import gradio as gr
import pandas as pd
from notenverwaltung.course import Course
from notenverwaltung.gradebook import GradeBook
from notenverwaltung.reports.text_report import TextReportGenerator
from notenverwaltung.student import Student

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

def generate_text_report(report_type: str, identifier: str) -> str:
    """Generate a text report for the selected report type."""
    gradebook = create_demo_gradebook()
    generator = TextReportGenerator(gradebook)

    if report_type == "Student":
        return generator.student_report(identifier)

    if report_type == "Course":
        return generator.course_report(identifier)

    if report_type == "Summary":
        return generator.summary_report()

    return "Unknown report type."

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


with gr.Blocks(title="Student Grade Tracker") as app:
    gr.Markdown("# Student Grade Tracker")
    gr.Markdown("Notenverwaltung mit Python, SQLite und Gradio")

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

        load_button.click(
            fn=load_table,
            inputs=table_selection,
            outputs=database_output,
        )
    
    with gr.Tab("Reports"):
        gr.Markdown("## Text Reports")

        report_type_input = gr.Radio(
            choices=["Student", "Course", "Summary"],
            value="Student",
            label="Report type",
        )

        identifier_input = gr.Textbox(
            value="S001",
            label="Student ID or Course ID",
            placeholder="Example: S001 or CS101",
        )

        report_button = gr.Button("Report erzeugen")

        report_output = gr.Textbox(
            label="Report",
            lines=12,
        )

        report_button.click(
            fn=generate_text_report,
            inputs=[report_type_input, identifier_input],
            outputs=report_output,
        )
        
if __name__ == "__main__":
    app.launch()