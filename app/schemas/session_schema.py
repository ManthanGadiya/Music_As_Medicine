from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class SessionCreate(BaseModel):
    participant_id: int
    therapist_id: int
    music_id: int
    session_date: date
    start_time: Optional[time] = None
    duration_min: int
    session_notes: Optional[str] = None


class SessionOut(BaseModel):
    session_id: int
    participant_id: int
    therapist_id: int
    music_id: int
    session_date: date
    start_time: Optional[time]
    duration_min: int
    session_notes: Optional[str]
