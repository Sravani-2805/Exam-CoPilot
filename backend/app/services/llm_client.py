"""
Thin LLM abstraction with THREE modes, chosen automatically from settings:

  1. LLM_PROVIDER=anthropic + LLM_API_KEY set   -> calls Anthropic's API (paid)
  2. LLM_PROVIDER=ollama                        -> calls a locally-running,
                                                    open-source model via Ollama
                                                    (free, no key, no internet
                                                    needed after the model is
                                                    pulled). See README section
                                                    "Free local LLM (Ollama)".
  3. Neither configured / reachable             -> deterministic template
                                                    responses so the rest of the
                                                    app is fully exercisable
                                                    with zero setup.
"""
import json
import httpx
from app.config import settings

try:
    import anthropic
except ImportError:
    anthropic = None


def _mode() -> str:
    if settings.llm_provider == "ollama":
        return "ollama"
    if settings.llm_provider == "anthropic" and settings.llm_api_key and anthropic is not None:
        return "anthropic"
    return "template"


def _call_anthropic(system: str, user: str) -> str:
    client = anthropic.Anthropic(api_key=settings.llm_api_key)
    resp = client.messages.create(
        model=settings.llm_model,
        max_tokens=1500,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in resp.content if block.type == "text")


def _call_ollama(system: str, user: str) -> str:
    """Calls a local Ollama server (default http://localhost:11434).
    Requires `ollama pull <model>` and `ollama serve` to be running first —
    see README for exact commands. LLM_MODEL should be an Ollama model name
    e.g. 'llama3.1', 'phi3', 'mistral', 'qwen2.5'."""
    base_url = settings.ollama_base_url
    resp = httpx.post(
        f"{base_url}/api/chat",
        json={
            "model": settings.llm_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def _call_llm(system: str, user: str) -> str | None:
    mode = _mode()
    try:
        if mode == "anthropic":
            return _call_anthropic(system, user)
        if mode == "ollama":
            return _call_ollama(system, user)
    except Exception as e:
        print(f"[llm_client] {mode} call failed, falling back to template: {e}")
    return None


def generate_explanation(topic_name: str, difficulty_level: str, student_notes: str | None = None) -> str:
    system = (
        "You are an expert tutor. Explain the given topic clearly at the "
        "requested difficulty level, with one worked example and one common "
        "mistake students make. Ground your answer in the student's notes if given."
    )
    user = f"Topic: {topic_name}\nLevel: {difficulty_level}\nStudent notes: {student_notes or 'none provided'}"

    result = _call_llm(system, user)
    if result:
        return result
    return (
        f"[Template explanation — set LLM_PROVIDER=ollama (free/local) or add an "
        f"LLM_API_KEY for real generation]\n\n"
        f"{topic_name} ({difficulty_level} level): This section would explain "
        f"the concept, walk through an example, and note common exam mistakes."
    )


def generate_quiz_questions(topic_name: str, num_questions: int, difficulty: str = "medium") -> list[dict]:
    system = (
        "You are a quiz generator for exam prep. Respond ONLY with a JSON array "
        "(no prose, no markdown fences) of objects with keys: question_type "
        "(mcq|true_false|short_answer|numerical), difficulty, question_text, "
        "options (array, only for mcq/true_false, else null), correct_answer, explanation."
    )
    user = f"Topic: {topic_name}\nNumber of questions: {num_questions}\nDifficulty: {difficulty}"

    raw = _call_llm(system, user)
    if raw:
        try:
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.strip("`")
                cleaned = cleaned[4:] if cleaned.lower().startswith("json") else cleaned
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return [{"question_type": "mcq", "difficulty": difficulty, "question_text": raw,
                      "options": [], "correct_answer": "", "explanation": "Model returned non-JSON; inspect raw output."}]

    return [
        {
            "question_type": "mcq",
            "difficulty": difficulty,
            "question_text": f"[Template Q{i+1}] Which statement about {topic_name} is correct?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explanation": "Set LLM_PROVIDER=ollama (free/local) or add LLM_API_KEY for real questions.",
        }
        for i in range(num_questions)
    ]


def grade_short_answer(question_text: str, correct_answer: str, student_answer: str) -> bool:
    """Only used for short_answer/numerical grading where exact match is unreliable."""
    system = "Grade the student's answer as correct or incorrect. Respond with exactly one word: CORRECT or INCORRECT."
    user = f"Question: {question_text}\nExpected answer: {correct_answer}\nStudent answer: {student_answer}"

    verdict = _call_llm(system, user)
    if verdict:
        return verdict.strip().upper().startswith("CORRECT")
    return student_answer.strip().lower() == correct_answer.strip().lower()
