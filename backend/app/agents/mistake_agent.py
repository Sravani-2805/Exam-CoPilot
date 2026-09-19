"""
Mistake Analysis Agent — blueprint section 14.

Rule-based first pass (works with zero LLM calls, so quiz feedback is
instant): classifies each wrong answer using simple heuristics on the
question metadata and answer text. This is intentionally conservative —
swap in an LLM classification call (see services/llm_client.py) for
richer diagnosis in Phase 3 without changing the interface.
"""
from app.models.quiz import QuizQuestion, Answer

MISTAKE_TYPES = ["conceptual", "recall", "calculation", "careless", "prerequisite_gap"]


def classify_mistake(question: QuizQuestion, student_answer: str) -> str:
    if not student_answer or not student_answer.strip():
        return "careless"  # left blank / no attempt

    qtype = question.question_type
    if qtype == "numerical":
        return "calculation"
    if qtype in ("mcq", "true_false"):
        # if the answer is a plausible option but wrong -> conceptual;
        # if wildly off-format -> careless. Heuristic on length/format similarity.
        if len(student_answer.strip()) <= 2:
            return "careless"
        return "conceptual"
    if qtype == "short_answer":
        # very short answers to a conceptual question usually indicate recall failure
        return "recall" if len(student_answer.split()) <= 3 else "conceptual"
    return "conceptual"


def analyze_attempt(answers: list[tuple[Answer, QuizQuestion]]) -> dict:
    """Returns a breakdown like {'conceptual': 2, 'recall': 1, ...} plus a
    one-line inference sentence, mirroring the blueprint's BCNF example."""
    breakdown = {k: 0 for k in MISTAKE_TYPES}
    wrong_topics_hint = []

    for answer, question in answers:
        if not answer.is_correct:
            mtype = answer.mistake_type or classify_mistake(question, answer.student_answer or "")
            breakdown[mtype] = breakdown.get(mtype, 0) + 1
            wrong_topics_hint.append(question.question_text[:40])

    dominant = max(breakdown, key=breakdown.get) if any(breakdown.values()) else None
    if dominant:
        inference = f"The student's errors are predominantly '{dominant}' type — recommend targeted remediation."
    else:
        inference = "No significant mistake pattern detected — performance is strong."

    return {"breakdown": breakdown, "inference": inference}
