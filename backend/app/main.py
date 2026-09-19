from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.config import settings
from app import models  # noqa: F401 — ensures all models are registered before create_all
from app.routers import auth, exams, syllabus, study_plan, quiz, progress, tutor

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ExamPilot API",
    description="Multi-Agent Adaptive Learning & Autonomous Exam Preparation Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(exams.router)
app.include_router(syllabus.router)
app.include_router(study_plan.router)
app.include_router(quiz.router)
app.include_router(progress.router)
app.include_router(tutor.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "ExamPilot API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
