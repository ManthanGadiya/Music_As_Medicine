from app.database import get_connection


def seed_therapist() -> None:
    with get_connection() as connection:
        existing = connection.execute(
            "SELECT therapist_id FROM Therapists WHERE contact_email = ?",
            ("therapist@mail.com",),
        ).fetchone()
        if existing:
            return
        connection.execute(
            """
            INSERT INTO Therapists (name, role, qualification, contact_email)
            VALUES (?, ?, ?, ?)
            """,
            ("Default Therapist", "Therapist", "Music Therapy Certification", "therapist@mail.com"),
        )


if __name__ == "__main__":
    seed_therapist()
