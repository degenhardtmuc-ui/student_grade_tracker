"""Registrierung und Anmeldung für den Student Grade Tracker."""

import hashlib
import hmac
import secrets
import sqlite3
from pathlib import Path


PBKDF2_ITERATIONS = 200_000


def _create_account_table(
    connection: sqlite3.Connection,
) -> None:
    """Lege die separate Tabelle für Zugangsdaten an."""

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS student_accounts (
            student_id TEXT PRIMARY KEY,
            password_salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            FOREIGN KEY (student_id)
                REFERENCES students(student_id)
                ON DELETE CASCADE
        )
        """
    )


def _hash_password(
    password: str,
    salt_hex: str,
) -> str:
    """Erzeuge aus Passwort und Salt einen sicheren Hash."""

    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        PBKDF2_ITERATIONS,
    ).hex()


def register_student(
    database_path: Path,
    student_id: str,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    password_repeat: str,
) -> str:
    """Registriere einen Studenten und speichere nur den Passwort-Hash."""

    student_id = student_id.strip().upper()
    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip().lower()

    if not all(
        [
            student_id,
            first_name,
            last_name,
            email,
            password,
        ]
    ):
        return "Bitte alle Felder ausfüllen."

    if "@" not in email:
        return "Bitte eine gültige E-Mail-Adresse eingeben."

    if len(password) < 8:
        return "Das Passwort muss mindestens 8 Zeichen lang sein."

    if password != password_repeat:
        return "Die beiden Passwörter stimmen nicht überein."

    salt_hex = secrets.token_hex(16)

    password_hash = _hash_password(
        password,
        salt_hex,
    )

    try:
        with sqlite3.connect(database_path) as connection:
            connection.execute(
                "PRAGMA foreign_keys = ON"
            )

            _create_account_table(connection)

            duplicate = connection.execute(
                """
                SELECT 1
                FROM students
                WHERE student_id = ?
                   OR LOWER(email) = ?
                """,
                (
                    student_id,
                    email,
                ),
            ).fetchone()

            if duplicate:
                return (
                    "Student-ID oder E-Mail-Adresse "
                    "ist bereits registriert."
                )

            connection.execute(
                """
                INSERT INTO students (
                    student_id,
                    first_name,
                    last_name,
                    email
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    student_id,
                    first_name,
                    last_name,
                    email,
                ),
            )

            connection.execute(
                """
                INSERT INTO student_accounts (
                    student_id,
                    password_salt,
                    password_hash
                )
                VALUES (?, ?, ?)
                """,
                (
                    student_id,
                    salt_hex,
                    password_hash,
                ),
            )

    except sqlite3.Error:
        return (
            "Registrierung fehlgeschlagen. "
            "Bitte Datenbank prüfen."
        )

    return (
        f"Registrierung erfolgreich. "
        f"{student_id} kann sich jetzt anmelden."
    )


def login_student(
    database_path: Path,
    student_id: str,
    password: str,
) -> str:
    """Prüfe Student-ID und Passwort ohne Klartextpasswort."""

    student_id = student_id.strip().upper()

    if not student_id or not password:
        return "Bitte Student-ID und Passwort eingeben."

    try:
        with sqlite3.connect(database_path) as connection:
            _create_account_table(connection)

            account = connection.execute(
                """
                SELECT
                    s.first_name,
                    s.last_name,
                    a.password_salt,
                    a.password_hash
                FROM student_accounts AS a
                JOIN students AS s
                    ON s.student_id = a.student_id
                WHERE a.student_id = ?
                """,
                (student_id,),
            ).fetchone()

    except sqlite3.Error:
        return (
            "Anmeldung fehlgeschlagen. "
            "Bitte Datenbank prüfen."
        )

    if account is None:
        return "Student-ID oder Passwort ist falsch."

    first_name = account[0]
    last_name = account[1]
    salt_hex = account[2]
    stored_hash = account[3]

    entered_hash = _hash_password(
        password,
        salt_hex,
    )

    if not hmac.compare_digest(
        entered_hash,
        stored_hash,
    ):
        return "Student-ID oder Passwort ist falsch."

    return (
        f"Anmeldung erfolgreich. "
        f"Willkommen, {first_name} {last_name}!"
    )