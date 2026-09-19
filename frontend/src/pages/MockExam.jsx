import React from "react";

export default function MockExam() {
  return (
    <div>
      <h1 className="text-2xl font-display font-bold text-white mb-4">Mock Exam</h1>
      <div className="bg-space-800 border border-space-700 rounded-2xl p-6 text-slate-400 text-sm">
        Full syllabus-aligned mock exam simulation — Phase 3 feature. Reuses
        the Quiz Agent (<code>agents/quiz_agent.py</code>) at larger scale
        across every topic in an exam, plus a timer and topic-wise report.
      </div>
    </div>
  );
}
