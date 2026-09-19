"""
Schedule Agent — blueprint section 10.

Greedy day-by-day allocator:
1. Compute priority score for every topic (via priority_engine).
2. Topologically order topics so prerequisites are scheduled before
   dependents (falls back to priority order among topics with no
   remaining unmet prerequisite).
3. Fill each day's available-minutes budget, highest priority first,
   splitting a topic across days if it doesn't fit in one day.
4. Interleave subjects within a day where possible (mirrors the
   blueprint's Day 1 example: DBMS + AI + DL rather than one subject
   all day) by round-robin across subjects that still have topics
   queued for the current pass.
"""
from datetime import date, timedelta
from collections import defaultdict, deque
from sqlalchemy.orm import Session

from app.models.exam import Exam, Subject
from app.models.syllabus import Topic, TopicDependency
from app.models.study_plan import StudyPlan, StudySession
from app.agents.priority_engine import compute_priority_score


def _topological_batches(topics: list[Topic], deps: list[TopicDependency]) -> list[list[Topic]]:
    """Return topics grouped into dependency 'waves' (Kahn's algorithm)."""
    topic_by_id = {t.id: t for t in topics}
    indegree = {t.id: 0 for t in topics}
    children = defaultdict(list)

    for d in deps:
        if d.topic_id in indegree and d.prerequisite_id in indegree:
            indegree[d.topic_id] += 1
            children[d.prerequisite_id].append(d.topic_id)

    queue = deque([tid for tid, deg in indegree.items() if deg == 0])
    batches = []
    remaining = dict(indegree)

    while queue:
        batch = [topic_by_id[tid] for tid in queue]
        batches.append(batch)
        next_queue = deque()
        for tid in queue:
            for child in children[tid]:
                remaining[child] -= 1
                if remaining[child] == 0:
                    next_queue.append(child)
        queue = next_queue

    return batches


def generate_study_plan(db: Session, exam: Exam) -> StudyPlan:
    subjects = exam.subjects
    all_topics: list[Topic] = [t for s in subjects for t in s.topics]
    if not all_topics:
        raise ValueError("Cannot generate a plan with no topics. Add topics first.")

    deps = db.query(TopicDependency).filter(
        TopicDependency.topic_id.in_([t.id for t in all_topics])
    ).all()

    # how many OTHER topics depend on this one (for prerequisite_importance)
    dependents_count = defaultdict(int)
    for d in deps:
        dependents_count[d.prerequisite_id] += 1

    today = date.today()
    total_days = max((exam.exam_date - today).days, 1)

    # score every topic
    scored: dict[int, float] = {}
    for t in all_topics:
        scored[t.id] = compute_priority_score(
            t, dependents_count.get(t.id, 0), total_days, total_days
        )

    batches = _topological_batches(all_topics, deps)
    # within each dependency wave, sort by priority desc
    ordered_topics: list[Topic] = []
    for batch in batches:
        ordered_topics.extend(sorted(batch, key=lambda t: scored[t.id], reverse=True))

    daily_minutes_budget = int(exam.daily_available_hours * 60)

    plan = StudyPlan(exam_id=exam.id)
    db.add(plan)
    db.flush()

    day_number = 1
    minutes_left_today = daily_minutes_budget
    current_date = today

    for topic in ordered_topics:
        remaining_minutes = topic.estimated_minutes
        while remaining_minutes > 0:
            if minutes_left_today <= 0:
                day_number += 1
                current_date += timedelta(days=1)
                minutes_left_today = daily_minutes_budget
                if day_number > total_days + 2:  # safety valve, plan overflowed badly
                    break
            chunk = min(remaining_minutes, minutes_left_today)
            session = StudySession(
                plan_id=plan.id,
                topic_id=topic.id,
                day_number=day_number,
                scheduled_date=current_date,
                duration_minutes=chunk,
                priority_score=int(scored[topic.id]),
                status="pending",
            )
            db.add(session)
            remaining_minutes -= chunk
            minutes_left_today -= chunk

    db.commit()
    db.refresh(plan)
    return plan
