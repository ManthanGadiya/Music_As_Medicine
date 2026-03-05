from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.participant_schema import ParticipantCreate
from app.services.analytics_service import participant_progress
from app.services.therapy_service import get_participant_sessions


router = APIRouter(prefix="/participants", tags=["participants"])


@router.post("")
def create_participant(payload: ParticipantCreate):
    created_at = datetime.now(tz=timezone.utc).isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO Participants (name, age, gender, category, special_need_type, medical_history, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.name,
                payload.age,
                payload.gender,
                payload.category,
                payload.special_need_type,
                payload.medical_history,
                created_at,
            ),
        )
        participant_id = cursor.lastrowid
        row = connection.execute(
            "SELECT * FROM Participants WHERE participant_id = ?",
            (participant_id,),
        ).fetchone()
    return {"data": dict(row)}


@router.get("")
def list_participants():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM Participants ORDER BY participant_id DESC"
        ).fetchall()
    return {"data": [dict(row) for row in rows]}


@router.get("/{participant_id}")
def get_participant(participant_id: int):
    with get_connection() as connection:
        participant = connection.execute(
            "SELECT * FROM Participants WHERE participant_id = ?",
            (participant_id,),
        ).fetchone()
    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return {"data": dict(participant)}


@router.get("/{participant_id}/sessions")
def participant_sessions(participant_id: int):
    with get_connection() as connection:
        exists = connection.execute(
            "SELECT participant_id FROM Participants WHERE participant_id = ?",
            (participant_id,),
        ).fetchone()
    if exists is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return {"data": get_participant_sessions(participant_id)}


@router.get("/{participant_id}/progress")
def participant_progress_report(participant_id: int):
    with get_connection() as connection:
        exists = connection.execute(
            "SELECT participant_id FROM Participants WHERE participant_id = ?",
            (participant_id,),
        ).fetchone()
    if exists is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return {"data": participant_progress(participant_id)}
