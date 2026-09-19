import React, { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { api } from "../services/api.js";

export default function Progress() {
  const [exams, setExams] = useState([]);
  const [examId, setExamId] = useState(null);
  const [mastery, setMastery] = useState([]);

  useEffect(() => {
    api.listExams().then((data) => {
      setExams(data);
      if (data.length) setExamId(data[0].id);
    });
  }, []);

  useEffect(() => {
    if (examId) api.getMastery(examId).then(setMastery);
  }, [examId]);

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-display font-bold text-white">Progress</h1>
        <select className="border border-space-600 rounded-xl p-2 text-sm" value={examId || ""} onChange={(e) => setExamId(Number(e.target.value))}>
          {exams.map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
        </select>
      </div>

      <div className="bg-space-800 border border-space-700 rounded-2xl p-4" style={{ height: 360 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={mastery}>
            <XAxis dataKey="topic_name" tick={{ fontSize: 11 }} />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Bar dataKey="overall" fill="#4f46e5" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
