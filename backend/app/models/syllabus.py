from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String, nullable=False)                     # e.g. "Normalization"
    unit = Column(String, nullable=True)                      # chapter/unit grouping
    exam_weight = Column(Float, default=5.0)                  # 0-10, marks weightage
    previous_paper_frequency = Column(Float, default=0.0)     # 0-10, how often it appears
    difficulty = Column(Float, default=5.0)                   # 0-10
    student_weakness = Column(Float, default=5.0)             # 0-10, higher = weaker
    estimated_minutes = Column(Integer, default=60)           # study duration estimate

    subject = relationship("Subject", back_populates="topics")
    mastery = relationship("MasteryScore", back_populates="topic", uselist=False, cascade="all, delete-orphan")


class TopicDependency(Base):
    """Edge in the topic dependency graph: topic_id requires prerequisite_id first."""
    __tablename__ = "topic_dependencies"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    prerequisite_id = Column(Integer, ForeignKey("topics.id"), nullable=False)


class Resource(Base):
    """Learning Resource Agent output: notes/examples/external links per topic."""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    type = Column(String, default="note")   # note | example | external_link | summary
    content = Column(Text, nullable=True)
    url = Column(String, nullable=True)


class Note(Base):
    """User-uploaded or AI-generated notes (feeds the RAG pipeline in Phase 3)."""
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    source_file = Column(String, nullable=True)   # path to uploaded PDF/PPT
