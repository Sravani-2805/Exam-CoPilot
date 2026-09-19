import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import Sidebar from "./components/Sidebar.jsx";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import MyExams from "./pages/MyExams.jsx";
import StudyPlan from "./pages/StudyPlan.jsx";
import Learn from "./pages/Learn.jsx";
import Quiz from "./pages/Quiz.jsx";
import Progress from "./pages/Progress.jsx";
import KnowledgeBase from "./pages/KnowledgeBase.jsx";
import MockExam from "./pages/MockExam.jsx";
import AIAssistant from "./pages/AIAssistant.jsx";
import Settings from "./pages/Settings.jsx";

function useIsAuthed() {
  const [authed, setAuthed] = useState(!!localStorage.getItem("access_token"));
  useEffect(() => {
    const check = () => setAuthed(!!localStorage.getItem("access_token"));
    window.addEventListener("storage", check);
    return () => window.removeEventListener("storage", check);
  }, []);
  return [authed, setAuthed];
}

function ProtectedLayout({ authed, setAuthed }) {
  const location = useLocation();
  if (!authed) return <Navigate to="/login" state={{ from: location }} replace />;

  return (
    <div className="min-h-screen bg-space-950 bg-nebula-radial">
      <div className="flex">
        <Sidebar onLogout={() => setAuthed(false)} />
        <main className="flex-1 min-h-screen">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/exams" element={<MyExams />} />
            <Route path="/study-plan" element={<StudyPlan />} />
            <Route path="/learn" element={<Learn />} />
            <Route path="/quiz" element={<Quiz />} />
            <Route path="/progress" element={<Progress />} />
            <Route path="/knowledge-base" element={<KnowledgeBase />} />
            <Route path="/mock-exam" element={<MockExam />} />
            <Route path="/assistant" element={<AIAssistant />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  const [authed, setAuthed] = useIsAuthed();

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={authed ? <Navigate to="/" replace /> : <Login onAuthed={() => setAuthed(true)} />}
        />
        <Route path="/*" element={<ProtectedLayout authed={authed} setAuthed={setAuthed} />} />
      </Routes>
    </BrowserRouter>
  );
}
