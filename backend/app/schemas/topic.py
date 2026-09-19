from pydantic import BaseModel
from typing import List, Optional


class TopicCreate(BaseModel):
    subject_id: int
    name: str
    unit: Optional[str] = None
    exam_weight: float = 5.0
    previous_paper_frequency: float = 0.0
    difficulty: float = 5.0
    student_weakness: float = 5.0
    estimated_minutes: int = 60
    prerequisite_ids: List[int] = []


class TopicOut(BaseModel):
    id: int
    name: str
    unit: Optional[str]
    exam_weight: float
    difficulty: float
    student_weakness: float
    estimated_minutes: int
    priority_score: Optional[float] = None

    class Config:
        from_attributes = True
