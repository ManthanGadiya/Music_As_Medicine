import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from app.config import DB_PATH


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS Participants (
    participant_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    gender VARCHAR(10),
    category VARCHAR(30),
    special_need_type VARCHAR(100),
    medical_history TEXT,
    created_at DATETIME
);

CREATE TABLE IF NOT EXISTS Therapists (
    therapist_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(50),
    qualification VARCHAR(100),
    contact_email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Music (
    music_id INTEGER PRIMARY KEY,
    title VARCHAR(100),
    genre VARCHAR(50),
    instrument VARCHAR(50),
    tempo FLOAT,
    frequency_range VARCHAR(50),
    duration_sec INTEGER,
    file_path TEXT
);

CREATE TABLE IF NOT EXISTS Sessions (
    session_id INTEGER PRIMARY KEY,
    participant_id INTEGER,
    therapist_id INTEGER,
    music_id INTEGER,
    session_date DATE,
    start_time TIME,
    duration_min INTEGER,
    session_notes TEXT,
    FOREIGN KEY (participant_id) REFERENCES Participants(participant_id),
    FOREIGN KEY (therapist_id) REFERENCES Therapists(therapist_id),
    FOREIGN KEY (music_id) REFERENCES Music(music_id)
);

CREATE TABLE IF NOT EXISTS PreSessionAssessment (
    pre_id INTEGER PRIMARY KEY,
    session_id INTEGER,
    mood_level INTEGER,
    stress_level INTEGER,
    attention_level INTEGER,
    notes TEXT,
    FOREIGN KEY (session_id) REFERENCES Sessions(session_id)
);

CREATE TABLE IF NOT EXISTS PostSessionFeedback (
    feedback_id INTEGER PRIMARY KEY,
    session_id INTEGER,
    mood_level INTEGER,
    behavior_change TEXT,
    attention_change TEXT,
    social_response TEXT,
    comments TEXT,
    FOREIGN KEY (session_id) REFERENCES Sessions(session_id)
);
"""


def initialize_database(db_path: Path = DB_PATH) -> None:
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.executescript(SCHEMA_SQL)
        connection.commit()
    finally:
        connection.close()


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()
