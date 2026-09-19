from pydantic import BaseModel


class MasteryOut(BaseModel):
    topic_id: int
    topic_name: str
    understanding: float
    recall: float
    application: float
    problem_solving: float
    overall: float

    class Config:
        from_attributes = True


class ReadinessOut(BaseModel):
    overall_readiness: float
    knowledge_mastery: float
    recall: float
    problem_solving: float
    consistency: float
    weak_topics: list[str]
    strong_topics: list[str]
