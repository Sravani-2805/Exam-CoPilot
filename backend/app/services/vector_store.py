"""
Phase 3 TODO — RAG vector store interface.

Define the interface now so Syllabus/Tutor agents can call it today;
implement with FAISS/Chroma/Qdrant later without touching call sites.
"""
from abc import ABC, abstractmethod


class VectorStore(ABC):
    @abstractmethod
    def add_document(self, doc_id: str, text: str, metadata: dict) -> None: ...

    @abstractmethod
    def query(self, text: str, top_k: int = 5) -> list[dict]: ...


class InMemoryVectorStore(VectorStore):
    """Placeholder: naive keyword-overlap 'retrieval' so the RAG code path
    is testable before a real embeddings model is wired in."""

    def __init__(self):
        self._docs: dict[str, dict] = {}

    def add_document(self, doc_id: str, text: str, metadata: dict) -> None:
        self._docs[doc_id] = {"text": text, "metadata": metadata}

    def query(self, text: str, top_k: int = 5) -> list[dict]:
        query_words = set(text.lower().split())
        scored = []
        for doc_id, doc in self._docs.items():
            overlap = len(query_words & set(doc["text"].lower().split()))
            if overlap:
                scored.append((overlap, doc_id, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"doc_id": d[1], **d[2]} for d in scored[:top_k]]


vector_store = InMemoryVectorStore()
