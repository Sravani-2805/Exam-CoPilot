"""
Intelligent Topic Priority Engine — blueprint section 9.

Priority Score = Exam Weight + Previous-Paper Frequency + Difficulty
                 + Student Weakness + Prerequisite Importance + Time Urgency

Each factor is normalized to 0-10 before weighting so no single input
(e.g. a badly-scaled "difficulty" import) can dominate the score.
"""
from dataclasses import dataclass
from datetime import date
from app.models.syllabus import Topic


@dataclass
class PriorityWeights:
    exam_weight: float = 1.0
    previous_paper_frequency: float = 1.0
    difficulty: float = 0.8
    student_weakness: float = 1.2
    prerequisite_importance: float = 0.6
    time_urgency: float = 1.0


DEFAULT_WEIGHTS = PriorityWeights()


def prerequisite_importance(topic: Topic, dependency_count_of_topic: int) -> float:
    """
    A topic that unlocks many downstream topics (i.e. many other topics
    depend on it) gets a higher prerequisite-importance score.
    `dependency_count_of_topic` = number of OTHER topics that list this
    topic as a prerequisite. Capped at 10.
    """
    return min(dependency_count_of_topic * 2.5, 10.0)


def time_urgency(days_remaining: int, total_days: int) -> float:
    """
    Rises as the exam approaches. Early in prep (lots of days remaining),
    urgency is low, allowing foundational topics to be scheduled first;
    it climbs sharply in the final third of the countdown.
    """
    if total_days <= 0:
        return 10.0
    fraction_elapsed = 1 - (days_remaining / total_days)
    return round(min(10.0, fraction_elapsed * 12), 2)  # accelerates near the end


def compute_priority_score(
    topic: Topic,
    dependency_count_of_topic: int,
    days_remaining: int,
    total_days: int,
    weights: PriorityWeights = DEFAULT_WEIGHTS,
) -> float:
    prereq_score = prerequisite_importance(topic, dependency_count_of_topic)
    urgency_score = time_urgency(days_remaining, total_days)

    raw = (
        topic.exam_weight * weights.exam_weight
        + topic.previous_paper_frequency * weights.previous_paper_frequency
        + topic.difficulty * weights.difficulty
        + topic.student_weakness * weights.student_weakness
        + prereq_score * weights.prerequisite_importance
        + urgency_score * weights.time_urgency
    )
    max_possible = 10 * sum(vars(weights).values())
    return round((raw / max_possible) * 100, 1)  # normalized 0-100


def priority_label(score: float) -> str:
    if score >= 75:
        return "Very High"
    if score >= 55:
        return "High"
    if score >= 35:
        return "Medium"
    return "Low"
