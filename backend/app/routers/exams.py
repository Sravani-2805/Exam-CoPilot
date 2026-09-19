from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.exam import Exam, Subject
from app.models.user import User
from app.schemas.exam import ExamCreate, ExamOut
from app.utils.security import get_current_user

router = APIRouter(prefix="/exams", tags=["exams"])


@router.post("", response_model=ExamOut)
def create_exam(payload: ExamCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exam = Exam(
        owner_id=user.id, name=payload.name, exam_date=payload.exam_date,
        daily_available_hours=payload.daily_available_hours,
    )
    db.add(exam)
    db.flush()
    for s in payload.subjects:
        db.add(Subject(exam_id=exam.id, name=s.name, self_reported_strength=s.self_reported_strength))
    db.commit()
    db.refresh(exam)
    return exam


@router.get("", response_model=list[ExamOut])
def list_exams(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Exam).filter(Exam.owner_id == user.id).all()


@router.get("/{exam_id}", response_model=ExamOut)
def get_exam(exam_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exam = db.query(Exam).get(exam_id)
    if not exam or exam.owner_id != user.id:
        raise HTTPException(404, "Exam not found")
    return exam
