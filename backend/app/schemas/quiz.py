from pydantic import BaseModel
from typing import List, Optional


class QuizQuestionOut(BaseModel):
    id: int
    question_type: str
    difficulty: str
    question_text: str
    options: Optional[List[str]] = None

    class Config:
        from_attributes = True


class QuizGenerateRequest(BaseModel):
    topic_id: int
    num_questions: int = 5


class AnswerSubmit(BaseModel):
    question_id: int
    student_answer: str


class QuizSubmitRequest(BaseModel):
    topic_id: int
    answers: List[AnswerSubmit]


class QuizResultOut(BaseModel):
    attempt_id: int
    score_percent: float
    mistake_breakdown: dict
    updated_mastery: dict
