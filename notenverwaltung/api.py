"""REST API for the Student Grade Tracker."""

import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Student Grade Tracker API",
    description=(
        "REST API für Studenten, Kurse und Noten."
    ),
    version="1.0.0",
)

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "grade_tracker.db"
)


class StudentResponse(BaseModel):
    """Public student data returned by the API."""

    student_id: str
    first_name: str
    last_name: str

@app.get(
    "/health",
    tags=["System"],
    summary="Prüfe den Zustand der API",
)
def health_check() -> dict[str, str]:
    """Bestätige, dass die REST API erreichbar ist."""

    return {
        "status": "ok",
        "service": "student-grade-tracker-api",
    }
@app.get(
    "/students",
    response_model=list[StudentResponse],
    tags=["Students"],
    summary="Lade alle Studenten",
)
def get_students() -> list[StudentResponse]:
    """Return all students stored in the SQLite database."""

    if not DATABASE_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Die Datenbank wurde nicht gefunden.",
        )

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute(
                """
                SELECT
                    student_id,
                    first_name,
                    last_name
                FROM students
                ORDER BY student_id
                """
            ).fetchall()

    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail="Der Datenbankzugriff ist fehlgeschlagen.",
        ) from error

    return [
        StudentResponse(
            student_id=row["student_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
        )
        for row in rows
    ]