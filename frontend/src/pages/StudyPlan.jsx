import React, { useEffect, useState } from "react";
import { api } from "../services/api.js";

export default function StudyPlan() {
  const [exams, setExams] = useState([]);
  const [examId, setExamId] = useState(null);
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.listExams().then((data) => {
      setExams(data);
      if (data.length) setExamId(data[0].id);
    });
  }, []);

  const loadPlan = (id) => api.getPlan(id).then(setPlan).catch(() => setPlan(null));
  useEffect(() => { if (examId) loadPlan(examId); }, [examId]);

  const handleGenerate = async () => {
    setError(null);
    try {
      await api.generatePlan(examId);
      loadPlan(examId);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleStatus = async (sessionId, status) => {
    await api.updateSessionStatus(sessionId, status);
    loadPlan(examId);
  };

  const days = {};
  (plan?.sessions || []).forEach((s) => {
    days[s.day_number] = days[s.day_number] || [];
    days[s.day_number].push(s);
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-display font-bold text-white">Study Plan</h1>
        <div className="flex gap-2">
          <select className="border border-space-600 rounded-xl p-2 text-sm" value={examId || ""} onChange={(e) => setExamId(Number(e.target.value))}>
            {exams.map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
          </select>
          <button onClick={handleGenerate} className="bg-nebula-gradient text-white px-4 py-2 rounded-lg text-sm font-medium">
            Generate / Replan
          </button>
        </div>
      </div>
      {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

      <div className="space-y-4">
        {Object.entries(days).sort((a, b) => a[0] - b[0]).map(([day, sessions]) => (
          <div key={day} className="bg-space-800 border border-space-700 rounded-2xl p-4">
            <div className="font-semibold mb-2">Day {day}</div>
            <ul className="space-y-2">
              {sessions.map((s) => (
                <li key={s.id} className="flex items-center justify-between text-sm border-b pb-2">
                  <span>{s.subject_name} — {s.topic_name} <span className="text-slate-400">({s.duration_minutes} min, priority {s.priority_score})</span></span>
                  <div className="flex gap-1">
                    <span className={`px-2 py-0.5 rounded text-xs ${s.status === "completed" ? "bg-green-100 text-green-700" : s.status === "missed" ? "bg-red-100 text-red-700" : "bg-slate-100 text-slate-300"}`}>{s.status}</span>
                    {s.status === "pending" && (
                      <>
                        <button onClick={() => handleStatus(s.id, "completed")} className="text-xs text-green-600 underline">Done</button>
                        <button onClick={() => handleStatus(s.id, "missed")} className="text-xs text-red-600 underline">Missed</button>
                      </>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
