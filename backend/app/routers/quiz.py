from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models.syllabus import Topic
from app.models.user import User
from app.schemas.quiz import QuizGenerateRequest, QuizQuestionOut, QuizSubmitRequest
from app.agents.quiz_agent import generate_quiz
from app.agents.orchestrator import handle_quiz_submission
from app.utils.security import get_current_user

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/generate", response_model=list[QuizQuestionOut])
def create_quiz(payload: QuizGenerateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    topic = db.query(Topic).get(payload.topic_id)
    if not topic or topic.subject.exam.owner_id != user.id:
        raise HTTPException(404, "Topic not found")

    questions = generate_quiz(db, topic, payload.num_questions)
    return [
        QuizQuestionOut(
            id=q.id, question_type=q.question_type, difficulty=q.difficulty,
            question_text=q.question_text,
            options=json.loads(q.options_json) if q.options_json else None,
        ) for q in questions
    ]


@router.post("/submit")
def submit_quiz(payload: QuizSubmitRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    topic = db.query(Topic).get(payload.topic_id)
    if not topic or topic.subject.exam.owner_id != user.id:
        raise HTTPException(404, "Topic not found")

    answers = [a.dict() for a in payload.answers]
    return handle_quiz_submission(db, user.id, payload.topic_id, answers)
