"""Notification Agent — blueprint section 26. Simple rule-based generator;
call this after replanning, quiz submission, or a daily cron tick."""
from datetime import date
from sqlalchemy.orm import Session
from app.models.mastery import Notification
from app.models.exam import Exam
from app.models.study_plan import StudySession


def generate_daily_notifications(db: Session, user_id: int, exam: Exam) -> list[Notification]:
    notifications = []
    days_left = (exam.exam_date - date.today()).days

    if days_left <= 3:
        notifications.append(Notification(
            user_id=user_id, category="urgent",
            message=f"Only {days_left} day(s) left for {exam.name}. Consider Emergency Exam Mode.",
        ))

    if exam.study_plan:
        missed = [s for s in exam.study_plan.sessions if s.status == "missed"]
        if missed:
            notifications.append(Notification(
                user_id=user_id, category="warning",
                message=f"{len(missed)} session(s) missed — plan has been auto-replanned.",
            ))

    for n in notifications:
        db.add(n)
    db.commit()
    return notifications
