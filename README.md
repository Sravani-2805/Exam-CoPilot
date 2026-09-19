# ExamPilot — Multi-Agent Adaptive Learning & Exam Prep Platform


## What's actually implemented (runs today)
- FastAPI backend with SQLAlchemy models for the full data model (users, exams,
  syllabus, topics, study plans, quizzes, mastery, revisions, notifications).
- A real **Priority Engine** (weighted scoring formula from the blueprint).
- A real **Schedule Agent** (greedy day-by-day allocator respecting daily hour
  budget, topic priority, and dependency ordering).
- A real **Mastery model** (per-topic understanding/recall/application/problem-solving).
- A real **Mistake Analysis Agent** (rule-based pattern detector: conceptual /
  recall / calculation / careless, extensible to LLM-based classification).
- A real **Replanning Agent** (recomputes remaining days when sessions are missed
  or mastery drops).
- An **Orchestrator** that wires agents together as plain Python — easy to later
  swap for LangGraph nodes (see `agents/orchestrator.py` comments for exactly
  where each maps to a LangGraph node).
- A **Quiz Agent** and **Tutor Agent** with an LLM client abstraction
  (`services/llm_client.py`) — plug in Anthropic/OpenAI API key and it generates
  real quizzes/explanations; without a key it returns deterministic template
  content so the app still runs end-to-end.
- REST routers exposing all of the above.
- React + Tailwind frontend skeleton with the 10 pages from the blueprint,
  wired to the API via `src/services/api.js`.

## What's stubbed (clearly marked `# TODO Phase 3/4`)
- RAG pipeline (chunking/embeddings/vector DB) — interface defined in
  `services/vector_store.py`, swap in FAISS/Chroma/Qdrant.
- Knowledge graph (Neo4j) — `Topic.prerequisites` already models the edges;
  swapping storage to Neo4j is a backend change only.
- Previous-paper analysis, flashcards, mock exam simulation, what-if simulator,
  calendar/Notion integration, voice mode, gamification.

## File structure
```
examplot/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entrypoint
│   │   ├── config.py                # env/settings
│   │   ├── database.py              # SQLAlchemy engine/session
│   │   ├── models/                  # ORM models (one file per entity group)
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── agents/                  # All 13 agents + orchestrator
│   │   ├── routers/                 # FastAPI route handlers
│   │   ├── services/                # llm_client, vector_store
│   │   └── utils/                   # security/auth helpers
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── pages/                   # Dashboard, MyExams, StudyPlan, Learn, Quiz,
│       │                             # Progress, KnowledgeBase, MockExam,
│       │                             # AIAssistant, Settings
│       ├── components/
│       └── services/api.js
├── docker-compose.yml
└── README.md
```

## Run it
```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # fill in DATABASE_URL, LLM_API_KEY, JWT_SECRET
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

Or via Docker:
```bash
docker-compose up --build
```

## Suggested next steps (in order)
1. Run migrations (add Alembic — not included to keep this scaffold light).
2. Plug a real LLM key into `.env` to activate Tutor/Quiz agent generation.
3. Add a PDF/PPT parser to `agents/syllabus_agent.py` (`# TODO Phase 1 parser`).
4. Add FAISS/Chroma to `services/vector_store.py` for RAG.
5. Move `agents/orchestrator.py` logic into LangGraph nodes 1:1 — the docstring
   in that file maps every function to a graph node already.
