"""
Orchestrator / Main Agent — blueprint section 4/5.

This file coordinates the agents as plain Python function calls. Each
public function below corresponds 1:1 to a node you'd create if you
migrate this to LangGraph — the mapping is:

    LangGraph node              ->  function here
    -----------------------------------------------------------
    "ingest_syllabus"           ->  syllabus_agent.create_topics_from_list
    "build_plan"                ->  schedule_agent.generate_study_plan
    "explain_topic"             ->  tutor_agent.explain_topic
    "generate_quiz"             ->  quiz_agent.generate_quiz
    "grade_quiz"                ->  quiz_agent.submit_quiz          (also
                                     internally calls mistake_agent +
                                     progress_agent)
    "compute_readiness"         ->  progress_agent.compute_readiness
    "replan"                    ->  replanning_agent.replan
    "notify"                    ->  notification_agent.generate_daily_notifications

To port to LangGraph: wrap each function as a node that reads/writes a
shared `AgentState` TypedDict, and use conditional edges where this file
currently uses plain `if` statements (see `handle_quiz_submission` below —
the "low score -> trigger replan" branch becomes a conditional edge).
"""
from sqlalchemy.orm import Session
from app.models.exam import Exam
from app.models.syllabus import Topic
from app.agents import schedule_agent, quiz_agent, replanning_agent, progress_agent, notification_agent

LOW_SCORE_REPLAN_THRESHOLD = 50.0


def handle_quiz_submission(db: Session, user_id: int, topic_id: int, answers: list[dict]) -> dict:
    """Runs Quiz Agent -> Mistake Agent -> Progress Agent, then decides
    whether the Replanning Agent should be invoked (agent-to-agent
    handoff, blueprint section 39)."""
    result = quiz_agent.submit_quiz(db, user_id, topic_id, answers)

    if result["score_percent"] < LOW_SCORE_REPLAN_THRESHOLD:
        topic = db.query(Topic).get(topic_id)
        exam = topic.subject.exam
        replanning_agent.replan(db, exam, boosted_topic_ids=[topic_id])
        result["replanned"] = True
    else:
        result["replanned"] = False

    return result


def handle_missed_session(db: Session, session_id: int) -> dict:
    session = replanning_agent.mark_session_status(db, session_id, "missed")
    exam = session.plan.exam
    notifications = notification_agent.generate_daily_notifications(db, exam.owner_id, exam)
    return {"session_id": session.id, "status": session.status,
            "notifications": [n.message for n in notifications]}


def build_initial_plan(db: Session, exam: Exam) -> dict:
    plan = schedule_agent.generate_study_plan(db, exam)
    notifications = notification_agent.generate_daily_notifications(db, exam.owner_id, exam)
    return {"plan_id": plan.id, "session_count": len(plan.sessions),
            "notifications": [n.message for n in notifications]}


def get_readiness_report(db: Session, exam_id: int) -> dict:
    return progress_agent.compute_readiness(db, exam_id)
