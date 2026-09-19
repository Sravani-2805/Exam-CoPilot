from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)

    exam = relationship("Exam", back_populates="study_plan")
    sessions = relationship("StudySession", back_populates="plan", cascade="all, delete-orphan")


class StudySession(Base):
    """A single scheduled block: Day N, Topic X, duration Y."""
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("study_plans.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    scheduled_date = Column(Date, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    priority_score = Column(Integer, default=0)
    status = Column(String, default="pending")  # pending | completed | postponed | missed

    plan = relationship("StudyPlan", back_populates="sessions")
