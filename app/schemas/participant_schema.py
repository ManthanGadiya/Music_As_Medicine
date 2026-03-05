from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ParticipantCreate(BaseModel):
    name: str = Field(max_length=100)
    age: int
    gender: str = Field(max_length=10)
    category: str = Field(max_length=30)
    special_need_type: Optional[str] = Field(default=None, max_length=100)
    medical_history: Optional[str] = None


class ParticipantOut(BaseModel):
    participant_id: int
    name: str
    age: int
    gender: str
    category: str
    special_need_type: Optional[str]
    medical_history: Optional[str]
    created_at: Optional[datetime]
