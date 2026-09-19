from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.exam import Exam
from app.models.study_plan import StudyPlan, StudySession
from app.models.user import User
from app.schemas.study_plan import StudyPlanOut, StudySessionOut, SessionStatusUpdate
from app.agents.orchestrator import build_initial_plan, handle_missed_session
from app.agents.replanning_agent import mark_session_status
from app.utils.security import get_current_user

router = APIRouter(prefix="/study-plan", tags=["study-plan"])


@router.post("/{exam_id}/generate")
def generate_plan(exam_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exam = db.query(Exam).get(exam_id)
    if not exam or exam.owner_id != user.id:
        raise HTTPException(404, "Exam not found")
    return build_initial_plan(db, exam)


@router.get("/{exam_id}", response_model=StudyPlanOut)
def get_plan(exam_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exam = db.query(Exam).get(exam_id)
    if not exam or exam.owner_id != user.id:
        raise HTTPException(404, "Exam not found")
    plan = db.query(StudyPlan).filter(StudyPlan.exam_id == exam_id).first()
    if not plan:
        raise HTTPException(404, "No plan generated yet")

    sessions_out = []
    for s in plan.sessions:
        sessions_out.append(StudySessionOut(
            id=s.id, day_number=s.day_number, scheduled_date=s.scheduled_date,
            topic_id=s.topic_id, topic_name=s.topic.name, subject_name=s.topic.subject.name,
            duration_minutes=s.duration_minutes, priority_score=s.priority_score, status=s.status,
        ))
    return StudyPlanOut(id=plan.id, exam_id=plan.exam_id, sessions=sessions_out)


@router.patch("/session/{session_id}")
def update_session_status(session_id: int, payload: SessionStatusUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(StudySession).get(session_id)
    if not session or session.plan.exam.owner_id != user.id:
        raise HTTPException(404, "Session not found")

    if payload.status == "missed":
        return handle_missed_session(db, session_id)
    return mark_session_status(db, session_id, payload.status)
