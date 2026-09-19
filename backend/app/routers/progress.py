from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.exam import Exam
from app.models.user import User
from app.schemas.mastery import MasteryOut, ReadinessOut
from app.agents.orchestrator import get_readiness_report
from app.utils.security import get_current_user

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/{exam_id}/mastery", response_model=list[MasteryOut])
def mastery_breakdown(exam_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exam = db.query(Exam).get(exam_id)
    if not exam or exam.owner_id != user.id:
        raise HTTPException(404, "Exam not found")

    out = []
    for subject in exam.subjects:
        for topic in subject.topics:
            if topic.mastery:
                m = topic.mastery
                out.append(MasteryOut(
                    topic_id=topic.id, topic_name=topic.name,
                    understanding=m.understanding, recall=m.recall,
                    application=m.application, problem_solving=m.problem_solving,
                    overall=m.overall,
                ))
    return out


@router.get("/{exam_id}/readiness", response_model=ReadinessOut)
def readiness(exam_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exam = db.query(Exam).get(exam_id)
    if not exam or exam.owner_id != user.id:
        raise HTTPException(404, "Exam not found")
    return get_readiness_report(db, exam_id)
