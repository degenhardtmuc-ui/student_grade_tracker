"""Registrierung und Anmeldung für den Student Grade Tracker."""

import hashlib
import hmac
import secrets
import sqlite3
from pathlib import Path


PBKDF2_ITERATIONS = 200_000

ALLOWED_ROLES = {
    "student",
    "teacher",
    "admin",
    "super_admin",
}

ASSIGNABLE_ROLES = {
    "student",
    "teacher",
    "admin",
}

def _create_account_table(
    connection: sqlite3.Connection,
) -> None:
    """Lege die Tabelle für Zugangsdaten und Benutzerrollen an."""

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS student_accounts (
            student_id TEXT PRIMARY KEY,
            password_salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student',
            FOREIGN KEY (student_id)
                REFERENCES students(student_id)
                ON DELETE CASCADE
        )
        """
    )

    columns = {
        row[1]
        for row in connection.execute(
            "PRAGMA table_info(student_accounts)"
        )
    }

    if "role" not in columns:
        connection.execute(
            """
            ALTER TABLE student_accounts
            ADD COLUMN role TEXT NOT NULL DEFAULT 'student'
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

def get_user_role_for_management(
    database_path: Path,
    acting_student_id: str,
    acting_role: str,
    target_student_id: str,
) -> tuple[str, str]:
    """Lese eine Benutzerrolle, wenn der Aufrufer Super-Admin ist."""

    acting_student_id = acting_student_id.strip().upper()
    target_student_id = target_student_id.strip().upper()

    if not acting_student_id or not acting_role:
        return "", "Bitte zuerst anmelden."

    if not target_student_id:
        return "", "Bitte einen Benutzer auswählen."

    try:
        with sqlite3.connect(database_path) as connection:
            _create_account_table(connection)

            acting_account = connection.execute(
                """
                SELECT role
                FROM student_accounts
                WHERE student_id = ?
                """,
                (acting_student_id,),
            ).fetchone()

            if (
                acting_role != "super_admin"
                or acting_account is None
                or acting_account[0] != "super_admin"
            ):
                return "", (
                    "Keine Berechtigung: Nur der Super-Admin "
                    "darf Rollen verwalten."
                )

            target_account = connection.execute(
                """
                SELECT role
                FROM student_accounts
                WHERE student_id = ?
                """,
                (target_student_id,),
            ).fetchone()

    except sqlite3.Error:
        return "", "Rolle konnte nicht geladen werden."

    if target_account is None:
        return "", "Benutzerkonto nicht gefunden."

    role = target_account[0]

    return (
        role,
        f"Aktuelle Rolle von {target_student_id}: {role}",
    )

def change_user_role(
    database_path: Path,
    acting_student_id: str,
    acting_role: str,
    target_student_id: str,
    new_role: str,
) -> tuple[str, str]:
    """Ändere eine Rolle ausschließlich als angemeldeter Super-Admin."""

    acting_student_id = acting_student_id.strip().upper()
    target_student_id = target_student_id.strip().upper()
    new_role = new_role.strip().lower()

    if not acting_student_id or not acting_role:
        return "", "Bitte zuerst anmelden."

    if not target_student_id:
        return "", "Bitte einen Benutzer auswählen."

    if new_role not in ASSIGNABLE_ROLES:
        return "", "Ungültige Rolle ausgewählt."

    try:
        with sqlite3.connect(database_path) as connection:
            _create_account_table(connection)

            acting_account = connection.execute(
                """
                SELECT role
                FROM student_accounts
                WHERE student_id = ?
                """,
                (acting_student_id,),
            ).fetchone()

            if (
                acting_role != "super_admin"
                or acting_account is None
                or acting_account[0] != "super_admin"
            ):
                return "", (
                    "Keine Berechtigung: Nur der Super-Admin "
                    "darf Rollen verwalten."
                )

            target_account = connection.execute(
                """
                SELECT role
                FROM student_accounts
                WHERE student_id = ?
                """,
                (target_student_id,),
            ).fetchone()

            if target_account is None:
                return "", "Benutzerkonto nicht gefunden."

            if target_account[0] == "super_admin":
                return "super_admin", (
                    "Der Super-Admin kann hier nicht verändert werden."
                )

            connection.execute(
                """
                UPDATE student_accounts
                SET role = ?
                WHERE student_id = ?
                """,
                (
                    new_role,
                    target_student_id,
                ),
            )

    except sqlite3.Error:
        return "", "Rollenänderung fehlgeschlagen."

    return (
        new_role,
        (
            f"Rolle erfolgreich geändert: "
            f"{target_student_id} ist jetzt {new_role}."
        ),
    )

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
                    a.password_hash,
                    a.role
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
    role = account[4]
    
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
        f"Willkommen, {first_name} {last_name}! "
        f"Rolle: {role}"
)