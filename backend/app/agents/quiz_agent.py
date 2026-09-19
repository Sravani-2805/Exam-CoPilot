"""
Quiz Agent — blueprint section 13. Generates adaptive quizzes and grades
them; difficulty for the NEXT quiz is chosen from the table in section 13.
"""
import json
from sqlalchemy.orm import Session
from app.models.quiz import QuizQuestion, QuizAttempt, Answer
from app.models.syllabus import Topic
from app.services.llm_client import generate_quiz_questions, grade_short_answer
from app.agents.mistake_agent import classify_mistake, analyze_attempt
from app.agents.progress_agent import update_mastery_from_attempt


def next_difficulty(last_score_percent: float | None) -> str:
    if last_score_percent is None:
        return "medium"
    if last_score_percent > 85:
        return "hard"
    if last_score_percent >= 60:
        return "medium"
    return "easy"


def generate_quiz(db: Session, topic: Topic, num_questions: int, last_score_percent: float | None = None) -> list[QuizQuestion]:
    difficulty = next_difficulty(last_score_percent)
    raw_questions = generate_quiz_questions(topic.name, num_questions, difficulty)

    questions = []
    for q in raw_questions:
        question = QuizQuestion(
            topic_id=topic.id,
            question_type=q.get("question_type", "mcq"),
            difficulty=q.get("difficulty", difficulty),
            question_text=q.get("question_text", ""),
            options_json=json.dumps(q.get("options")) if q.get("options") else None,
            correct_answer=q.get("correct_answer", ""),
            explanation=q.get("explanation", ""),
        )
        db.add(question)
        questions.append(question)
    db.commit()
    return questions


def submit_quiz(db: Session, user_id: int, topic_id: int, answers: list[dict]) -> dict:
    """answers = [{'question_id': int, 'student_answer': str}, ...]"""
    attempt = QuizAttempt(user_id=user_id, topic_id=topic_id, score_percent=0.0)
    db.add(attempt)
    db.flush()

    graded_pairs = []
    correct_count = 0
    for a in answers:
        question = db.query(QuizQuestion).get(a["question_id"])
        if not question:
            continue
        if question.question_type in ("mcq", "true_false"):
            is_correct = a["student_answer"].strip().lower() == question.correct_answer.strip().lower()
        else:
            is_correct = grade_short_answer(question.question_text, question.correct_answer, a["student_answer"])

        mistake_type = None if is_correct else classify_mistake(question, a["student_answer"])
        answer_row = Answer(
            attempt_id=attempt.id,
            question_id=question.id,
            student_answer=a["student_answer"],
            is_correct=int(is_correct),
            mistake_type=mistake_type,
        )
        db.add(answer_row)
        graded_pairs.append((answer_row, question))
        correct_count += int(is_correct)

    total = len(graded_pairs) or 1
    attempt.score_percent = round(correct_count / total * 100, 1)
    db.commit()

    mistake_report = analyze_attempt(graded_pairs)
    mastery = update_mastery_from_attempt(db, topic_id, graded_pairs)

    return {
        "attempt_id": attempt.id,
        "score_percent": attempt.score_percent,
        "mistake_breakdown": mistake_report["breakdown"],
        "inference": mistake_report["inference"],
        "updated_mastery": {
            "understanding": mastery.understanding,
            "recall": mastery.recall,
            "application": mastery.application,
            "problem_solving": mastery.problem_solving,
            "overall": mastery.overall,
        },
    }
