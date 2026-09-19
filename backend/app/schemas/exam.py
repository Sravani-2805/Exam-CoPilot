from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class SubjectCreate(BaseModel):
    name: str
    self_reported_strength: str = "average"   # weak | average | strong


class ExamCreate(BaseModel):
    name: str
    exam_date: date
    daily_available_hours: float = 4.0
    subjects: List[SubjectCreate]


class ExamOut(BaseModel):
    id: int
    name: str
    exam_date: date
    daily_available_hours: float

    class Config:
        from_attributes = True
