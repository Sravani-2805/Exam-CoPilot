"""
Syllabus Intelligence Agent — blueprint section 7.

Phase 1 implementation: accepts already-structured topic input from the
frontend (manual entry form) — this is enough to exercise the full
pipeline end-to-end. Phase 1 TODO parser: wire in pypdf/python-pptx to
extract raw text from an uploaded file, then either (a) ask the LLM to
propose a topic list in JSON, or (b) run simple heading-detection regex
as a zero-LLM-cost fallback. Both should funnel into `create_topics_from_list`.
"""
from sqlalchemy.orm import Session
from app.models.syllabus import Topic, TopicDependency
from app.models.exam import Subject


def create_topics_from_list(db: Session, subject: Subject, topic_specs: list[dict]) -> list[Topic]:
    """
    topic_specs: [{"name": "Normalization", "unit": "Unit 2", "exam_weight": 8,
                    "difficulty": 6, "prerequisite_names": ["ER Model"]}, ...]
    """
    created: dict[str, Topic] = {}
    for spec in topic_specs:
        topic = Topic(
            subject_id=subject.id,
            name=spec["name"],
            unit=spec.get("unit"),
            exam_weight=spec.get("exam_weight", 5.0),
            previous_paper_frequency=spec.get("previous_paper_frequency", 0.0),
            difficulty=spec.get("difficulty", 5.0),
            student_weakness=spec.get("student_weakness", 5.0),
            estimated_minutes=spec.get("estimated_minutes", 60),
        )
        db.add(topic)
        db.flush()
        created[topic.name] = topic

    db.commit()

    # second pass: wire up prerequisite edges now that all topics have IDs
    for spec in topic_specs:
        for prereq_name in spec.get("prerequisite_names", []):
            prereq = created.get(prereq_name)
            topic = created.get(spec["name"])
            if prereq and topic:
                db.add(TopicDependency(topic_id=topic.id, prerequisite_id=prereq.id))
    db.commit()

    return list(created.values())


# TODO Phase 1 parser — example of where a real parser plugs in:
# def extract_topics_from_pdf(file_path: str) -> list[dict]:
#     from pypdf import PdfReader
#     text = "\n".join(page.extract_text() for page in PdfReader(file_path).pages)
#     # ... heading detection or LLM call to turn `text` into topic_specs ...
#     return topic_specs
