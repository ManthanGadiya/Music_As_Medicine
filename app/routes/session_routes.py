from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.feedback_schema import PostFeedbackCreate, PreAssessmentCreate
from app.schemas.session_schema import SessionCreate
from app.utils.validation_utils import validate_mood_scale


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("")
def start_session(payload: SessionCreate):
    with get_connection() as connection:
        participant = connection.execute(
            "SELECT participant_id FROM Participants WHERE participant_id = ?",
            (payload.participant_id,),
        ).fetchone()
        therapist = connection.execute(
            "SELECT therapist_id FROM Therapists WHERE therapist_id = ?",
            (payload.therapist_id,),
        ).fetchone()
        music = connection.execute(
            "SELECT music_id FROM Music WHERE music_id = ?",
            (payload.music_id,),
        ).fetchone()

        if participant is None:
            raise HTTPException(status_code=400, detail="Invalid participant_id")
        if therapist is None:
            raise HTTPException(status_code=400, detail="Invalid therapist_id")
        if music is None:
            raise HTTPException(status_code=400, detail="Invalid music_id")

        cursor = connection.execute(
            """
            INSERT INTO Sessions (participant_id, therapist_id, music_id, session_date, start_time, duration_min, session_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.participant_id,
                payload.therapist_id,
                payload.music_id,
                payload.session_date.isoformat(),
                payload.start_time.isoformat() if payload.start_time else None,
                payload.duration_min,
                payload.session_notes,
            ),
        )
        session_id = cursor.lastrowid
        session = connection.execute("SELECT * FROM Sessions WHERE session_id = ?", (session_id,)).fetchone()
    return {"data": dict(session)}


@router.get("/{session_id}")
def get_session(session_id: int):
    with get_connection() as connection:
        session = connection.execute(
            "SELECT * FROM Sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")

        pre = connection.execute(
            "SELECT * FROM PreSessionAssessment WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        post = connection.execute(
            "SELECT * FROM PostSessionFeedback WHERE session_id = ?",
            (session_id,),
        ).fetchone()

    return {
        "data": {
            "session": dict(session),
            "pre_assessment": dict(pre) if pre else None,
            "post_feedback": dict(post) if post else None,
        }
    }


@router.post("/{session_id}/pre-assessment")
def submit_pre_assessment(session_id: int, payload: PreAssessmentCreate):
    validate_mood_scale(payload.mood_level, "mood_level")
    validate_mood_scale(payload.stress_level, "stress_level")
    validate_mood_scale(payload.attention_level, "attention_level")

    with get_connection() as connection:
        session = connection.execute(
            "SELECT session_id FROM Sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")

        existing = connection.execute(
            "SELECT pre_id FROM PreSessionAssessment WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Pre-assessment already exists for this session")

        cursor = connection.execute(
            """
            INSERT INTO PreSessionAssessment (session_id, mood_level, stress_level, attention_level, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, payload.mood_level, payload.stress_level, payload.attention_level, payload.notes),
        )
        pre_id = cursor.lastrowid
        row = connection.execute("SELECT * FROM PreSessionAssessment WHERE pre_id = ?", (pre_id,)).fetchone()
    return {"data": dict(row)}


@router.post("/{session_id}/feedback")
def submit_feedback(session_id: int, payload: PostFeedbackCreate):
    validate_mood_scale(payload.mood_level, "mood_level")

    with get_connection() as connection:
        session = connection.execute(
            "SELECT session_id FROM Sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")

        existing = connection.execute(
            "SELECT feedback_id FROM PostSessionFeedback WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Feedback already exists for this session")

        cursor = connection.execute(
            """
            INSERT INTO PostSessionFeedback (session_id, mood_level, behavior_change, attention_change, social_response, comments)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                payload.mood_level,
                payload.behavior_change,
                payload.attention_change,
                payload.social_response,
                payload.comments,
            ),
        )
        feedback_id = cursor.lastrowid
        row = connection.execute(
            "SELECT * FROM PostSessionFeedback WHERE feedback_id = ?",
            (feedback_id,),
        ).fetchone()
    return {"data": dict(row)}
