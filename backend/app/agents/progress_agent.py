"""
Progress & Mastery Agent — blueprint section 15.

Updates the 4-dimension mastery model after each quiz attempt using a
simple exponential-moving-average so a single bad quiz doesn't crater
mastery, but recent performance is weighted more heavily than old data.
"""
from sqlalchemy.orm import Session
from app.models.mastery import MasteryScore
from app.models.quiz import QuizQuestion, Answer

ALPHA = 0.35  # weight given to the NEW observation vs. existing mastery


def _dimension_deltas(question: QuizQuestion, is_correct: bool) -> dict:
    """Maps a question's type to which mastery dimension(s) it exercises."""
    score = 100.0 if is_correct else 0.0
    mapping = {
        "mcq": {"understanding": score, "recall": score * 0.6},
        "true_false": {"understanding": score, "recall": score * 0.4},
        "short_answer": {"recall": score, "understanding": score * 0.7},
        "numerical": {"application": score, "problem_solving": score},
        "coding": {"application": score, "problem_solving": score},
        "case_based": {"application": score, "problem_solving": score * 0.8, "understanding": score * 0.5},
    }
    return mapping.get(question.question_type, {"understanding": score})


def update_mastery_from_attempt(db: Session, topic_id: int, graded_answers: list[tuple[Answer, QuizQuestion]]) -> MasteryScore:
    mastery = db.query(MasteryScore).filter(MasteryScore.topic_id == topic_id).first()
    if not mastery:
        mastery = MasteryScore(topic_id=topic_id, understanding=50, recall=50, application=50, problem_solving=50)
        db.add(mastery)
        db.flush()

    accum = {"understanding": [], "recall": [], "application": [], "problem_solving": []}
    for answer, question in graded_answers:
        deltas = _dimension_deltas(question, bool(answer.is_correct))
        for dim, val in deltas.items():
            accum[dim].append(val)

    for dim, values in accum.items():
        if not values:
            continue
        observed = sum(values) / len(values)
        current = getattr(mastery, dim)
        updated = (1 - ALPHA) * current + ALPHA * observed
        setattr(mastery, dim, round(updated, 1))

    db.commit()
    db.refresh(mastery)
    return mastery


def compute_readiness(db: Session, exam_id: int) -> dict:
    """Aggregates mastery across every topic in the exam into a readiness report
    (blueprint section 18)."""
    from app.models.exam import Exam

    exam = db.query(Exam).get(exam_id)
    all_scores: list[MasteryScore] = []
    topic_names = {}
    for subject in exam.subjects:
        for topic in subject.topics:
            if topic.mastery:
                all_scores.append(topic.mastery)
                topic_names[topic.mastery.id] = topic.name

    if not all_scores:
        return {
            "overall_readiness": 0, "knowledge_mastery": 0, "recall": 0,
            "problem_solving": 0, "consistency": 0, "weak_topics": [], "strong_topics": [],
        }

    avg = lambda field: round(sum(getattr(m, field) for m in all_scores) / len(all_scores), 1)
    overall_scores = [m.overall for m in all_scores]
    consistency = round(100 - (max(overall_scores) - min(overall_scores)), 1) if len(overall_scores) > 1 else 100.0

    weak = [topic_names[m.id] for m in all_scores if m.overall < 60]
    strong = [topic_names[m.id] for m in all_scores if m.overall >= 80]

    return {
        "overall_readiness": round(sum(overall_scores) / len(overall_scores), 1),
        "knowledge_mastery": avg("understanding"),
        "recall": avg("recall"),
        "problem_solving": avg("problem_solving"),
        "consistency": max(consistency, 0.0),
        "weak_topics": weak,
        "strong_topics": strong,
    }
