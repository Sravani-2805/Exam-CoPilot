import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Rocket, Mail, Lock, Eye, EyeOff, ArrowRight, BookOpen, Brain } from "lucide-react";
import { api } from "../services/api.js";

export default function Login({ onAuthed }) {
  const [mode, setMode] = useState("login"); // login | register
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      if (mode === "register") {
        await api.register(email, password, fullName);
        await api.login(email, password);
      } else {
        await api.login(email, password);
      }
      onAuthed?.();
      navigate("/");
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-space-950 bg-nebula-radial flex">
      {/* Left hero panel */}
      <div className="hidden lg:flex flex-col justify-center flex-1 px-16 relative overflow-hidden">
        {/* shooting star accent */}
        <div className="absolute top-24 right-24 w-32 h-px bg-gradient-to-r from-transparent via-nebula-400 to-transparent rotate-[-20deg] opacity-60" />

        <div className="flex items-center gap-2 absolute top-10 left-16">
          <div className="w-9 h-9 rounded-xl bg-nebula-gradient flex items-center justify-center">
            <Rocket size={18} className="text-white" />
          </div>
          <span className="font-display font-bold text-xl text-white">ExamPilot</span>
        </div>

        <div className="max-w-md">
          <p className="text-slate-400 font-body mb-2">Welcome to</p>
          <h1 className="font-display font-extrabold text-5xl bg-nebula-gradient bg-clip-text text-transparent mb-4 leading-tight">
            ExamPilot
          </h1>
          <p className="text-slate-400 font-body leading-relaxed">
            Your AI-powered co-pilot for exam success.<br />
            Plan smarter. Learn better.{" "}
            <span className="text-nebula-400">Ace with confidence.</span>
          </p>
        </div>

        {/* illustration: open book + floating brain/chart card */}
        <div className="relative mt-16 w-full max-w-md h-64">
          <div className="absolute bottom-0 left-0 w-72 h-40 bg-gradient-to-t from-nebula-500/30 to-transparent rounded-full blur-2xl" />
          <div className="absolute bottom-4 left-4 flex items-end gap-1 text-nebula-400">
            <BookOpen size={120} strokeWidth={1} className="text-nebula-400/80 drop-shadow-[0_0_25px_rgba(124,58,237,0.35)]" />
          </div>
          <div className="absolute top-2 right-6 bg-space-800/80 border border-space-600 rounded-2xl p-4 backdrop-blur-sm shadow-glow">
            <Brain size={28} className="text-nebula-400 mb-2" />
            <div className="text-xs text-slate-400">Overall Readiness</div>
            <div className="text-2xl font-display font-bold text-white">78%</div>
          </div>
        </div>
      </div>

      {/* Right auth card */}
      <div className="flex items-center justify-center flex-1 px-6 py-12">
        <div className="w-full max-w-md bg-space-800/90 border border-space-600 rounded-2xl p-8 shadow-glow backdrop-blur-sm">
          <div className="lg:hidden flex items-center gap-2 mb-6">
            <div className="w-8 h-8 rounded-lg bg-nebula-gradient flex items-center justify-center">
              <Rocket size={16} className="text-white" />
            </div>
            <span className="font-display font-bold text-lg text-white">ExamPilot</span>
          </div>

          <h2 className="font-display font-bold text-2xl text-white mb-1">
            {mode === "login" ? "Welcome Back! 👋" : "Create your account"}
          </h2>
          <p className="text-slate-400 text-sm mb-6">
            {mode === "login" ? "Login to continue your learning journey." : "Start your personalized exam prep journey."}
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === "register" && (
              <div>
                <label className="text-sm text-slate-300 mb-1 block">Full name</label>
                <input
                  className="w-full bg-space-900 border border-space-600 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-nebula-500"
                  placeholder="Your name"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                />
              </div>
            )}

            <div>
              <label className="text-sm text-slate-300 mb-1 block">Email</label>
              <div className="relative">
                <Mail size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="email"
                  required
                  className="w-full bg-space-900 border border-space-600 rounded-xl pl-11 pr-4 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-nebula-500"
                  placeholder="youremail@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>

            <div>
              <label className="text-sm text-slate-300 mb-1 block">Password</label>
              <div className="relative">
                <Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  className="w-full bg-space-900 border border-space-600 rounded-xl pl-11 pr-11 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-nebula-500"
                  placeholder="••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button type="button" onClick={() => setShowPassword((s) => !s)}
                        className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300">
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {mode === "login" && (
              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center gap-2 text-slate-400">
                  <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)}
                         className="rounded border-space-600 bg-space-900 text-nebula-500 focus:ring-nebula-500" />
                  Remember me
                </label>
                <span className="text-nebula-400 cursor-pointer hover:underline">Forgot password?</span>
              </div>
            )}

            {error && <p className="text-sm text-red-400">{error}</p>}

            <button type="submit" disabled={loading}
                    className="w-full bg-nebula-gradient text-white font-medium rounded-xl py-3 flex items-center justify-center gap-2 hover:opacity-90 transition disabled:opacity-50">
              {loading ? "Please wait..." : mode === "login" ? "Login" : "Create account"}
              <ArrowRight size={16} />
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-slate-400">
            {mode === "login" ? (
              <>New here? <button onClick={() => setMode("register")} className="text-nebula-400 font-medium hover:underline">Create an account</button></>
            ) : (
              <>Already have an account? <button onClick={() => setMode("login")} className="text-nebula-400 font-medium hover:underline">Log in</button></>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
