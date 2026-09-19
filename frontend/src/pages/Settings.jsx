import React from "react";
import { useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";

export default function Settings() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <div className="p-8 max-w-md">
      <h1 className="font-display font-bold text-2xl text-white mb-6">Settings</h1>
      <div className="bg-space-800 border border-space-700 rounded-2xl p-6">
        <div className="text-sm text-slate-400 mb-4">
          Profile, integrations and notification settings will live here.
        </div>
        <button
          onClick={handleLogout}
          className="flex items-center gap-2 text-red-400 border border-red-400/30 rounded-xl px-4 py-2.5 text-sm font-medium hover:bg-red-400/10"
        >
          <LogOut size={16} /> Log out
        </button>
      </div>
    </div>
  );
}
