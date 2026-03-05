from typing import Any, Dict, List

from app.database import get_connection


def participant_progress(participant_id: int) -> List[Dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                s.session_id,
                s.session_date,
                pre.mood_level AS pre_mood_level,
                post.mood_level AS post_mood_level,
                post.behavior_change,
                post.attention_change,
                post.social_response
            FROM Sessions s
            LEFT JOIN PreSessionAssessment pre ON pre.session_id = s.session_id
            LEFT JOIN PostSessionFeedback post ON post.session_id = s.session_id
            WHERE s.participant_id = ?
            ORDER BY s.session_date ASC, s.session_id ASC
            """,
            (participant_id,),
        )
        return [dict(row) for row in cursor.fetchall()]
