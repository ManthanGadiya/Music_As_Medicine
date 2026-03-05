from typing import Optional

from pydantic import BaseModel


class PreAssessmentCreate(BaseModel):
    mood_level: int
    stress_level: int
    attention_level: int
    notes: Optional[str] = None


class PostFeedbackCreate(BaseModel):
    mood_level: int
    behavior_change: Optional[str] = None
    attention_change: Optional[str] = None
    social_response: Optional[str] = None
    comments: Optional[str] = None
