import React, { useState } from "react";

export default function AIAssistant() {
  const [messages, setMessages] = useState([
    { role: "assistant", text: "Hi! I'm your ExamPilot assistant. Ask me about your plan, a topic, or your progress." },
  ]);
  const [input, setInput] = useState("");

  const send = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", text: input }]);
    setInput("");
    // TODO: wire to a conversational endpoint that routes to the Orchestrator
    // (e.g. intent classification -> call explain_topic / get_readiness_report / etc.)
  };

  return (
    <div className="max-w-2xl p-8">
      <h1 className="text-2xl font-display font-bold text-white mb-4">AI Assistant</h1>
      <div className="bg-space-800 border border-space-700 rounded-2xl p-4 h-96 overflow-y-auto space-y-2 mb-3">
        {messages.map((m, i) => (
          <div key={i} className={`text-sm p-2 rounded-lg max-w-[80%] ${m.role === "user" ? "bg-indigo-50 ml-auto" : "bg-slate-100"}`}>
            {m.text}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input className="flex-1 border border-space-600 rounded-xl p-2 text-sm" value={input}
               onChange={(e) => setInput(e.target.value)} placeholder="Ask something..."
               onKeyDown={(e) => e.key === "Enter" && send()} />
        <button onClick={send} className="bg-nebula-gradient text-white px-4 py-2 rounded-lg text-sm font-medium">Send</button>
      </div>
    </div>
  );
}
