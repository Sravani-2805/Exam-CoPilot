"""
Subject / Tutor Agent — blueprint section 12.
Generates a difficulty-appropriate explanation for a topic, optionally
grounded in the student's uploaded notes via the vector store.
"""
from sqlalchemy.orm import Session
from app.models.syllabus import Topic
from app.services.llm_client import generate_explanation
from app.services.vector_store import vector_store


def explain_topic(db: Session, topic: Topic, level: str = "intermediate") -> str:
    retrieved = vector_store.query(topic.name, top_k=3)
    grounding = "\n".join(r["text"][:300] for r in retrieved) if retrieved else None
    return generate_explanation(topic.name, level, student_notes=grounding)
