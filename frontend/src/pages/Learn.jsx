import React, { useState } from "react";
import { api } from "../services/api.js";

export default function Learn() {
  const [topicId, setTopicId] = useState("");
  const [level, setLevel] = useState("intermediate");
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleExplain = async () => {
    setLoading(true);
    try {
      const res = await api.explainTopic(Number(topicId), level);
      setExplanation(res.explanation);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl p-8">
      <h1 className="text-2xl font-display font-bold text-white mb-4">Learn</h1>
      <div className="bg-space-800 border border-space-700 rounded-2xl p-4 space-y-3">
        <input className="w-full border border-space-600 rounded-xl p-2" placeholder="Topic ID"
               value={topicId} onChange={(e) => setTopicId(e.target.value)} />
        <select className="w-full border border-space-600 rounded-xl p-2" value={level} onChange={(e) => setLevel(e.target.value)}>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
        <button onClick={handleExplain} disabled={!topicId || loading}
                className="bg-nebula-gradient text-white px-4 py-2 rounded-lg text-sm font-medium disabled:opacity-50">
          {loading ? "Thinking..." : "Explain this topic"}
        </button>
      </div>

      {explanation && (
        <div className="bg-space-800 border border-space-700 rounded-2xl p-4 mt-4 whitespace-pre-wrap text-sm">
          {explanation}
        </div>
      )}
    </div>
  );
}
