from typing import Any, Dict, List

from app.database import get_connection


def list_music() -> List[Dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.execute("SELECT * FROM Music ORDER BY music_id DESC")
        return [dict(row) for row in cursor.fetchall()]
