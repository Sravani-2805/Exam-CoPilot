import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Gauge, Clock, GraduationCap, ListChecks, ChevronRight, Play,
  Sparkles, Flame, PlusCircle, HelpCircle, FileCheck2, Library,
} from "lucide-react";
import { api } from "../services/api.js";

function StatCard({ icon: Icon, iconBg, label, value }) {
  return (
    <div className="bg-space-800 border border-space-700 rounded-2xl p-5 flex-1 min-w-[150px]">
      <div className={`w-9 h-9 rounded-xl flex items-center justify-center mb-3 ${iconBg}`}>
        <Icon size={18} className="text-white" />
      </div>
      <div className="text-xs text-slate-400 mb-1">{label}</div>
      <div className="text-2xl font-display font-bold text-white">{value}</div>
    </div>
  );
}

export default function Dashboard() {
  const [exams, setExams] = useState([]);
  const [selectedExamId, setSelectedExamId] = useState(null);
  const [plan, setPlan] = useState(null);
  const [readiness, setReadiness] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.listExams().then((data) => {
      setExams(data);
      if (data.length) setSelectedExamId(data[0].id);
    });
  }, []);

  useEffect(() => {
    if (!selectedExamId) return;
    api.getPlan(selectedExamId).then(setPlan).catch(() => setPlan(null));
    api.getReadiness(selectedExamId).then(setReadiness).catch(() => setReadiness(null));
  }, [selectedExamId]);

  const todaySessions = (plan?.sessions || []).filter((s) => s.day_number === 1);
  const completedMinutes = (plan?.sessions || [])
    .filter((s) => s.status === "completed")
    .reduce((sum, s) => sum + s.duration_minutes, 0);
  const studyHours = (completedMinutes / 60).toFixed(1);

  const daysLeft = (examDate) => {
    const diff = Math.ceil((new Date(examDate) - new Date()) / (1000 * 60 * 60 * 24));
    return diff >= 0 ? diff : 0;
  };

  return (
    <div className="p-8">
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="font-display font-bold text-2xl text-white">Good day! 👋</h1>
          <p className="text-slate-400 text-sm mt-1">Ready to conquer today's goals?</p>
        </div>
        <div className="bg-space-800 border border-nebula-500/40 rounded-xl px-4 py-2 flex items-center gap-2 text-orange-400 text-sm font-medium">
          <Flame size={16} />
          Keep it up
        </div>
      </div>

      <div className="flex gap-4 flex-wrap mb-8">
        <StatCard icon={Gauge} iconBg="bg-emerald-500/80" label="Overall Readiness"
                  value={readiness ? `${readiness.overall_readiness}%` : "—"} />
        <StatCard icon={Clock} iconBg="bg-nebula-500/80" label="Study Hours" value={`${studyHours}h`} />
        <StatCard icon={GraduationCap} iconBg="bg-nebula-pink/80" label="Exams" value={exams.length} />
        <StatCard icon={ListChecks} iconBg="bg-amber-500/80" label="Sessions Done"
                  value={(plan?.sessions || []).filter((s) => s.status === "completed").length} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2 bg-space-800 border border-space-700 rounded-2xl p-6">
          <div className="font-display font-semibold text-white mb-4">Today's Plan</div>

          {todaySessions.length === 0 && (
            <div className="text-sm text-slate-400 py-6 text-center">
              No sessions yet.{" "}
              <button onClick={() => navigate("/study-plan")} className="text-nebula-400 hover:underline">
                Generate your study plan
              </button>{" "}
              to see today's tasks here.
            </div>
          )}

          <div className="space-y-3">
            {todaySessions.map((s) => (
              <div key={s.id} className="flex items-center justify-between bg-space-900 border border-space-700 rounded-xl px-4 py-3">
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-2 h-2 rounded-full bg-nebula-400 shrink-0" />
                  <div className="min-w-0">
                    <div className="text-sm font-medium text-white truncate">{s.subject_name} — {s.topic_name}</div>
                    <div className="text-xs text-slate-500">{s.duration_minutes} min</div>
                  </div>
                </div>
                <button onClick={() => navigate("/study-plan")}
                        className="w-8 h-8 rounded-full bg-nebula-gradient flex items-center justify-center shrink-0">
                  <Play size={14} className="text-white" />
                </button>
              </div>
            ))}
          </div>

          {todaySessions.length > 0 && (
            <button onClick={() => navigate("/study-plan")}
                    className="w-full mt-4 flex items-center justify-center gap-1 text-sm text-slate-300 border border-space-700 rounded-xl py-2.5 hover:bg-space-900">
              View Full Plan <ChevronRight size={14} />
            </button>
          )}
        </div>

        <div className="bg-space-800 border border-space-700 rounded-2xl p-6 flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles size={18} className="text-nebula-400" />
            <span className="font-display font-semibold text-white">AI Insight</span>
          </div>
          <p className="text-sm text-slate-400 flex-1">
            {readiness?.weak_topics?.length
              ? <>Focus more on <span className="text-nebula-400 font-medium">{readiness.weak_topics[0]}</span> — it's currently your weakest area.</>
              : "Generate a study plan and take a few quizzes to unlock personalized insights here."}
          </p>
          <button onClick={() => navigate("/assistant")}
                  className="mt-4 w-full bg-nebula-gradient text-white text-sm font-medium rounded-xl py-2.5 flex items-center justify-center gap-2">
            <Sparkles size={14} /> Ask AI Assistant
          </button>
        </div>
      </div>

      <div className="bg-space-800 border border-space-700 rounded-2xl p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <div className="font-display font-semibold text-white">Upcoming Exams</div>
          <button onClick={() => navigate("/exams")} className="text-sm text-nebula-400 hover:underline">View All</button>
        </div>
        {exams.length === 0 ? (
          <div className="text-sm text-slate-400 text-center py-6">No exams yet — create your first one.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {exams.slice(0, 3).map((e) => (
              <div key={e.id} className="bg-space-900 border border-space-700 rounded-xl p-4">
                <div className="text-sm font-medium text-white mb-1">{e.name}</div>
                <div className="text-xs text-slate-500 mb-3">{e.exam_date}</div>
                <div className="text-xs text-nebula-400 font-medium">{daysLeft(e.exam_date)} Days Left</div>
                <div className="w-full h-1.5 bg-space-700 rounded-full mt-2 overflow-hidden">
                  <div className="h-full bg-nebula-gradient" style={{ width: `${Math.min(100, 100 - daysLeft(e.exam_date))}%` }} />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="bg-space-800 border border-space-700 rounded-2xl p-6">
        <div className="font-display font-semibold text-white mb-4">Quick Actions</div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <QuickAction icon={PlusCircle} label="Create" sub="Study Plan" onClick={() => navigate("/study-plan")} />
          <QuickAction icon={HelpCircle} label="Start" sub="Quiz" onClick={() => navigate("/quiz")} />
          <QuickAction icon={FileCheck2} label="Take" sub="Mock Exam" onClick={() => navigate("/mock-exam")} />
          <QuickAction icon={Library} label="Browse" sub="Resources" onClick={() => navigate("/knowledge-base")} />
        </div>
      </div>
    </div>
  );
}

function QuickAction({ icon: Icon, label, sub, onClick }) {
  return (
    <button onClick={onClick}
            className="flex items-center gap-3 bg-space-900 border border-space-700 rounded-xl p-4 hover:border-nebula-500 transition text-left">
      <div className="w-9 h-9 rounded-lg bg-nebula-gradient flex items-center justify-center shrink-0">
        <Icon size={16} className="text-white" />
      </div>
      <div className="min-w-0">
        <div className="text-sm text-white font-medium">{label}</div>
        <div className="text-xs text-slate-500">{sub}</div>
      </div>
    </button>
  );
}
