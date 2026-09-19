import React, { useState } from "react";
import { api } from "../services/api.js";

export default function Quiz() {
  const [topicId, setTopicId] = useState("");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  const handleGenerate = async () => {
    setResult(null);
    const qs = await api.generateQuiz(Number(topicId), 5);
    setQuestions(qs);
    setAnswers({});
  };

  const handleSubmit = async () => {
    const payload = questions.map((q) => ({ question_id: q.id, student_answer: answers[q.id] || "" }));
    const res = await api.submitQuiz(Number(topicId), payload);
    setResult(res);
  };

  return (
    <div className="max-w-2xl p-8">
      <h1 className="text-2xl font-display font-bold text-white mb-4">Quiz</h1>
      <div className="bg-space-800 border border-space-700 rounded-2xl p-4 space-y-3 mb-4">
        <input className="w-full border border-space-600 rounded-xl p-2" placeholder="Topic ID"
               value={topicId} onChange={(e) => setTopicId(e.target.value)} />
        <button onClick={handleGenerate} disabled={!topicId}
                className="bg-nebula-gradient text-white px-4 py-2 rounded-lg text-sm font-medium disabled:opacity-50">
          Generate Quiz
        </button>
      </div>

      {questions.map((q, i) => (
        <div key={q.id} className="bg-space-800 border border-space-700 rounded-2xl p-4 mb-3">
          <div className="font-medium mb-2">{i + 1}. {q.question_text}</div>
          {q.options ? (
            <div className="space-y-1">
              {q.options.map((opt) => (
                <label key={opt} className="flex items-center gap-2 text-sm">
                  <input type="radio" name={`q-${q.id}`} value={opt}
                         onChange={(e) => setAnswers({ ...answers, [q.id]: e.target.value })} />
                  {opt}
                </label>
              ))}
            </div>
          ) : (
            <input className="w-full border border-space-600 rounded-xl p-2 text-sm"
                   onChange={(e) => setAnswers({ ...answers, [q.id]: e.target.value })} />
          )}
        </div>
      ))}

      {questions.length > 0 && (
        <button onClick={handleSubmit} className="bg-emerald-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
          Submit Quiz
        </button>
      )}

      {result && (
        <div className="bg-space-800 border border-space-700 rounded-2xl p-4 mt-4 text-sm">
          <div className="font-semibold mb-1">Score: {result.score_percent}%</div>
          <div className="text-slate-300 mb-2">{result.inference}</div>
          <div className="text-slate-400">Mistake breakdown: {JSON.stringify(result.mistake_breakdown)}</div>
          {result.replanned && <div className="text-red-600 mt-2">Score was low — your remaining plan was auto-replanned.</div>}
        </div>
      )}
    </div>
  );
}
