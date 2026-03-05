from datetime import UTC, date, datetime

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


def seed_minimum_10_rows() -> None:
    with get_connection() as connection:
        participant_count = connection.execute("SELECT COUNT(*) FROM Participants").fetchone()[0]
        for i in range(participant_count + 1, 11):
            connection.execute(
                """
                INSERT INTO Participants (name, age, gender, category, special_need_type, medical_history, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"Participant {i}",
                    6 + i,
                    "Male" if i % 2 else "Female",
                    "special_child" if i % 2 else "neurotypical",
                    "Autism" if i % 2 else None,
                    f"Medical history note {i}",
                    datetime.now(UTC).isoformat(),
                ),
            )

        therapist_count = connection.execute("SELECT COUNT(*) FROM Therapists").fetchone()[0]
        for i in range(therapist_count + 1, 11):
            connection.execute(
                """
                INSERT INTO Therapists (name, role, qualification, contact_email)
                VALUES (?, ?, ?, ?)
                """,
                (f"Therapist {i}", "Therapist", "Music Therapy Certification", f"therapist{i}@mail.com"),
            )

        music_count = connection.execute("SELECT COUNT(*) FROM Music").fetchone()[0]
        for i in range(music_count + 1, 11):
            connection.execute(
                """
                INSERT INTO Music (title, genre, instrument, tempo, frequency_range, duration_sec, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"Track {i}",
                    "instrumental" if i % 2 else "meditation",
                    "piano" if i % 2 else "flute",
                    50.0 + i,
                    "low" if i % 2 else "mid",
                    300 + i * 20,
                    f"/music/track_{i}.mp3",
                ),
            )

        session_count = connection.execute("SELECT COUNT(*) FROM Sessions").fetchone()[0]
        for i in range(session_count + 1, 11):
            connection.execute(
                """
                INSERT INTO Sessions (participant_id, therapist_id, music_id, session_date, start_time, duration_min, session_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    i,
                    i,
                    i,
                    date(2026, 3, min(i, 28)).isoformat(),
                    "10:00:00",
                    20 + i,
                    f"Therapy session note {i}",
                ),
            )

        pre_count = connection.execute("SELECT COUNT(*) FROM PreSessionAssessment").fetchone()[0]
        for i in range(pre_count + 1, 11):
            connection.execute(
                """
                INSERT INTO PreSessionAssessment (session_id, mood_level, stress_level, attention_level, notes)
                VALUES (?, ?, ?, ?, ?)
                """,
                (i, (i % 10) + 1, ((i + 2) % 10) + 1, ((i + 4) % 10) + 1, f"Pre-assessment note {i}"),
            )

        post_count = connection.execute("SELECT COUNT(*) FROM PostSessionFeedback").fetchone()[0]
        for i in range(post_count + 1, 11):
            connection.execute(
                """
                INSERT INTO PostSessionFeedback (session_id, mood_level, behavior_change, attention_change, social_response, comments)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    i,
                    ((i + 5) % 10) + 1,
                    f"Behavior improved {i}",
                    f"Attention improved {i}",
                    f"Social response improved {i}",
                    f"Post-session comments {i}",
                ),
            )


if __name__ == "__main__":
    seed_therapist()
    seed_minimum_10_rows()
