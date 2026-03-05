from typing import Any, Dict, List

from app.database import get_connection


def get_participant_sessions(participant_id: int) -> List[Dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT s.*
            FROM Sessions s
            WHERE s.participant_id = ?
            ORDER BY s.session_date DESC, s.session_id DESC
            """,
            (participant_id,),
        )
        return [dict(row) for row in cursor.fetchall()]
