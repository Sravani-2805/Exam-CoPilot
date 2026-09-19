import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  Rocket, LayoutDashboard, GraduationCap, CalendarDays, BookOpenText,
  HelpCircle, TrendingUp, Library, FileCheck2, Sparkles, Settings as SettingsIcon,
  MoreVertical, LogOut,
} from "lucide-react";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/exams", label: "My Exams", icon: GraduationCap },
  { to: "/study-plan", label: "Study Plan", icon: CalendarDays },
  { to: "/learn", label: "Learn", icon: BookOpenText },
  { to: "/quiz", label: "Quiz", icon: HelpCircle },
  { to: "/progress", label: "Progress", icon: TrendingUp },
  { to: "/knowledge-base", label: "Knowledge Base", icon: Library },
  { to: "/mock-exam", label: "Mock Exam", icon: FileCheck2 },
  { to: "/assistant", label: "AI Assistant", icon: Sparkles },
  { to: "/settings", label: "Settings", icon: SettingsIcon },
];

export default function Sidebar({ userLabel = "Student", onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    onLogout?.();
    navigate("/login");
  };

  return (
    <aside className="w-64 shrink-0 bg-space-900 border-r border-space-700 min-h-screen flex flex-col p-4">
      <div className="flex items-center gap-2 px-2 mb-8 mt-1">
        <div className="w-9 h-9 rounded-xl bg-nebula-gradient flex items-center justify-center">
          <Rocket size={18} className="text-white" />
        </div>
        <span className="font-display font-bold text-lg text-white">ExamPilot</span>
      </div>

      <nav className="flex-1 flex flex-col gap-1">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition ${
                isActive
                  ? "bg-nebula-gradient text-white shadow-glow"
                  : "text-slate-400 hover:bg-space-800 hover:text-white"
              }`
            }
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="mt-4 flex items-center justify-between bg-space-800 border border-space-700 rounded-xl p-3">
        <div className="flex items-center gap-2 min-w-0">
          <div className="w-9 h-9 rounded-full bg-nebula-gradient flex items-center justify-center text-white text-sm font-semibold shrink-0">
            {userLabel.slice(0, 1).toUpperCase()}
          </div>
          <div className="min-w-0">
            <div className="text-sm font-medium text-white truncate">{userLabel}</div>
            <div className="text-xs text-nebula-400">Free Plan</div>
          </div>
        </div>
        <button onClick={handleLogout} title="Log out" className="text-slate-500 hover:text-white shrink-0">
          <LogOut size={16} />
        </button>
      </div>
    </aside>
  );
}
