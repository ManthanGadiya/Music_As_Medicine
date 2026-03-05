from fastapi import APIRouter

from app.database import get_connection
from app.schemas.music_schema import MusicCreate
from app.services.music_service import list_music


router = APIRouter(prefix="/music", tags=["music"])


@router.get("")
def get_music_library():
    return {"data": list_music()}


@router.post("")
def add_music(payload: MusicCreate):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO Music (title, genre, instrument, tempo, frequency_range, duration_sec, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.title,
                payload.genre,
                payload.instrument,
                payload.tempo,
                payload.frequency_range,
                payload.duration_sec,
                payload.file_path,
            ),
        )
        music_id = cursor.lastrowid
        row = connection.execute("SELECT * FROM Music WHERE music_id = ?", (music_id,)).fetchone()
    return {"data": dict(row)}
