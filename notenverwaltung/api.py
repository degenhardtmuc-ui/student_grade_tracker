"""REST API for the Student Grade Tracker."""

from fastapi import FastAPI


app = FastAPI(
    title="Student Grade Tracker API",
    description=(
        "REST API für Studenten, Kurse und Noten."
    ),
    version="1.0.0",
)


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