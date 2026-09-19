"""
Replanning Agent — blueprint section 10 / 39.

Triggered when:
  - a session is marked 'missed' or 'postponed'
  - mastery for a topic drops below a threshold after a quiz
  - available daily hours change

Strategy: delete all *future* (not yet completed) sessions in the plan
and re-run the Schedule Agent, but with student_weakness bumped for any
topic that just triggered replanning, and with the exam's remaining
days recalculated from today. Completed sessions are left untouched so
history/progress isn't lost.
"""
from datetime import date
from sqlalchemy.orm import Session

from app.models.study_plan import StudyPlan, StudySession
from app.models.exam import Exam
from app.agents.schedule_agent import generate_study_plan


def replan(db: Session, exam: Exam, boosted_topic_ids: list[int] | None = None) -> StudyPlan:
    plan = db.query(StudyPlan).filter(StudyPlan.exam_id == exam.id).first()
    if plan:
        # keep completed sessions as history; drop everything else
        db.query(StudySession).filter(
            StudySession.plan_id == plan.id,
            StudySession.status != "completed",
        ).delete(synchronize_session=False)
        db.commit()

    if boosted_topic_ids:
        for subject in exam.subjects:
            for topic in subject.topics:
                if topic.id in boosted_topic_ids:
                    topic.student_weakness = min(10.0, topic.student_weakness + 2.0)
        db.commit()

    # if a plan row already exists, generate_study_plan would create a
    # duplicate — reuse the existing plan id by deleting the empty shell first
    if plan and not db.query(StudySession).filter(StudySession.plan_id == plan.id).first():
        db.delete(plan)
        db.commit()

    return generate_study_plan(db, exam)


def mark_session_status(db: Session, session_id: int, status: str) -> StudySession:
    session = db.query(StudySession).get(session_id)
    if not session:
        raise ValueError("Session not found")
    session.status = status
    db.commit()
    db.refresh(session)

    if status == "missed":
        exam = session.plan.exam
        replan(db, exam, boosted_topic_ids=[session.topic_id])

    return session
