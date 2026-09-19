from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.exam import Exam, Subject
from app.models.user import User
from app.schemas.topic import TopicCreate, TopicOut
from app.agents.syllabus_agent import create_topics_from_list
from app.utils.security import get_current_user

router = APIRouter(prefix="/syllabus", tags=["syllabus"])


@router.post("/topics", response_model=list[TopicOut])
def add_topics(topics: list[TopicCreate], db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not topics:
        raise HTTPException(400, "No topics provided")
    subject = db.query(Subject).get(topics[0].subject_id)
    if not subject or subject.exam.owner_id != user.id:
        raise HTTPException(404, "Subject not found")

    id_to_name = {}
    specs = []
    for t in topics:
        specs.append({
            "name": t.name, "unit": t.unit, "exam_weight": t.exam_weight,
            "previous_paper_frequency": t.previous_paper_frequency, "difficulty": t.difficulty,
            "student_weakness": t.student_weakness, "estimated_minutes": t.estimated_minutes,
            "prerequisite_names": [],  # simple create; use /topics/with-deps for prereqs by name
        })
    created = create_topics_from_list(db, subject, specs)
    return created


@router.get("/topics/{subject_id}", response_model=list[TopicOut])
def list_topics(subject_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    subject = db.query(Subject).get(subject_id)
    if not subject or subject.exam.owner_id != user.id:
        raise HTTPException(404, "Subject not found")
    return subject.topics
