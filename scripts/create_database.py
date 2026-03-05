import sqlite3
from pathlib import Path

from app.database import SCHEMA_SQL


DB_PATH = Path(__file__).resolve().parents[1] / "music_therapy.db"


def initialize_database() -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.executescript(SCHEMA_SQL)

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at: {DB_PATH}")
