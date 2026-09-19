import React, { useEffect, useState } from "react";
import { api } from "../services/api.js";

export default function MyExams() {
  const [exams, setExams] = useState([]);
  const [name, setName] = useState("");
  const [examDate, setExamDate] = useState("");
  const [hours, setHours] = useState(4);
  const [subjects, setSubjects] = useState("DBMS, AI, Deep Learning, Compiler Design");
  const [error, setError] = useState(null);

  const load = () => api.listExams().then(setExams).catch((e) => setError(e.message));
  useEffect(() => { load(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await api.createExam({
        name,
        exam_date: examDate,
        daily_available_hours: Number(hours),
        subjects: subjects.split(",").map((s) => ({ name: s.trim(), self_reported_strength: "average" })),
      });
      setName(""); setExamDate("");
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="max-w-2xl p-8">
      <h1 className="text-2xl font-display font-bold text-white mb-4">My Exams</h1>

      <form onSubmit={handleCreate} className="bg-space-800 p-4 rounded-xl border mb-6 space-y-3">
        <input className="w-full border border-space-600 rounded-xl p-2" placeholder="Exam name (e.g. End Semester)"
               value={name} onChange={(e) => setName(e.target.value)} required />
        <input className="w-full border border-space-600 rounded-xl p-2" type="date"
               value={examDate} onChange={(e) => setExamDate(e.target.value)} required />
        <input className="w-full border border-space-600 rounded-xl p-2" type="number" min="1" max="16"
               value={hours} onChange={(e) => setHours(e.target.value)} placeholder="Daily hours" />
        <input className="w-full border border-space-600 rounded-xl p-2" value={subjects}
               onChange={(e) => setSubjects(e.target.value)} placeholder="Subjects, comma-separated" />
        <button className="bg-nebula-gradient text-white px-4 py-2 rounded-lg text-sm font-medium">
          Create Exam
        </button>
        {error && <p className="text-red-600 text-sm">{error}</p>}
      </form>

      <div className="space-y-2">
        {exams.map((e) => (
          <div key={e.id} className="bg-space-800 p-4 rounded-xl border flex justify-between">
            <div>
              <div className="font-semibold">{e.name}</div>
              <div className="text-sm text-slate-400">Exam date: {e.exam_date}</div>
            </div>
            <div className="text-sm text-slate-400">{e.daily_available_hours} hrs/day</div>
          </div>
        ))}
      </div>
    </div>
  );
}
