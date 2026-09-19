from pydantic import BaseModel
from datetime import date
from typing import Optional


class StudySessionOut(BaseModel):
    id: int
    day_number: int
    scheduled_date: Optional[date]
    topic_id: int
    topic_name: Optional[str] = None
    subject_name: Optional[str] = None
    duration_minutes: int
    priority_score: int
    status: str

    class Config:
        from_attributes = True


class StudyPlanOut(BaseModel):
    id: int
    exam_id: int
    sessions: list[StudySessionOut]

    class Config:
        from_attributes = True


class SessionStatusUpdate(BaseModel):
    status: str  # completed | postponed | missed
