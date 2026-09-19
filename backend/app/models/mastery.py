from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class MasteryScore(Base):
    """Topic-level mastery across 4 dimensions, per blueprint section 15."""
    __tablename__ = "mastery_scores"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), unique=True, nullable=False)
    understanding = Column(Float, default=0.0)
    recall = Column(Float, default=0.0)
    application = Column(Float, default=0.0)
    problem_solving = Column(Float, default=0.0)

    topic = relationship("Topic", back_populates="mastery")

    @property
    def overall(self) -> float:
        return round(
            (self.understanding + self.recall + self.application + self.problem_solving) / 4, 1
        )


class RevisionSchedule(Base):
    __tablename__ = "revision_schedules"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    reason = Column(String, default="spaced_review")  # spaced_review | forgetting_risk | mistake_followup
    completed = Column(Boolean, default=False)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    category = Column(String, default="info")  # info | warning | urgent
    is_read = Column(Boolean, default=False)
