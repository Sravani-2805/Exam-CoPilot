from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)              # e.g. "End Semester"
    exam_date = Column(Date, nullable=False)
    daily_available_hours = Column(Float, default=4.0)

    owner = relationship("User", back_populates="exams")
    subjects = relationship("Subject", back_populates="exam", cascade="all, delete-orphan")
    study_plan = relationship("StudyPlan", back_populates="exam", uselist=False, cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    name = Column(String, nullable=False)               # e.g. "DBMS"
    self_reported_strength = Column(String, default="average")  # weak / average / strong

    exam = relationship("Exam", back_populates="subjects")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
