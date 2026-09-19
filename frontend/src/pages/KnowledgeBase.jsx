import React from "react";

export default function KnowledgeBase() {
  return (
    <div>
      <h1 className="text-2xl font-display font-bold text-white mb-4">Knowledge Base</h1>
      <div className="bg-space-800 border border-space-700 rounded-2xl p-6 text-slate-400 text-sm">
        Notion-like workspace (Notes, Documents, Concepts, Flashcards, Questions) —
        Phase 3/4 feature. Backend models for Notes/Resources already exist
        (<code>app/models/syllabus.py</code>); this page wires up once the RAG
        pipeline (<code>app/services/vector_store.py</code>) is implemented.
      </div>
    </div>
  );
}
