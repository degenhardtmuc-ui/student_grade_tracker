"""Gradio user interface for the Student Grade Tracker."""

import sqlite3
from pathlib import Path

import gradio as gr
import pandas as pd


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


if __name__ == "__main__":
    app.launch()