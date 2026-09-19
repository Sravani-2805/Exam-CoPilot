from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.syllabus import Topic
from app.models.user import User
from app.agents.tutor_agent import explain_topic
from app.utils.security import get_current_user

router = APIRouter(prefix="/tutor", tags=["tutor"])


class ExplainRequest(BaseModel):
    topic_id: int
    level: str = "intermediate"  # beginner | intermediate | advanced


@router.post("/explain")
def explain(payload: ExplainRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    topic = db.query(Topic).get(payload.topic_id)
    if not topic or topic.subject.exam.owner_id != user.id:
        raise HTTPException(404, "Topic not found")
    return {"topic": topic.name, "level": payload.level, "explanation": explain_topic(db, topic, payload.level)}
