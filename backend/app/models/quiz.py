from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    question_type = Column(String, default="mcq")  # mcq | true_false | short_answer | numerical | coding
    difficulty = Column(String, default="medium")   # easy | medium | hard
    question_text = Column(Text, nullable=False)
    options_json = Column(Text, nullable=True)      # JSON-encoded list for MCQ
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    score_percent = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    answers = relationship("Answer", back_populates="attempt", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    student_answer = Column(Text, nullable=True)
    is_correct = Column(Integer, default=0)  # 0/1
    mistake_type = Column(String, nullable=True)  # conceptual | recall | calculation | careless | prerequisite_gap

    attempt = relationship("QuizAttempt", back_populates="answers")
