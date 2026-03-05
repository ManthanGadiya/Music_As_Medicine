from app.database import get_connection


def load_sample_music() -> None:
    tracks = [
        ("Calm Piano", "instrumental", "piano", 60.0, "low", 600, "/music/piano_calm.mp3"),
        ("Soft Flute", "meditation", "flute", 55.0, "mid", 480, "/music/flute_soft.mp3"),
    ]
    with get_connection() as connection:
        for track in tracks:
            exists = connection.execute(
                "SELECT music_id FROM Music WHERE title = ? AND file_path = ?",
                (track[0], track[6]),
            ).fetchone()
            if exists:
                continue
            connection.execute(
                """
                INSERT INTO Music (title, genre, instrument, tempo, frequency_range, duration_sec, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                track,
            )


if __name__ == "__main__":
    load_sample_music()
