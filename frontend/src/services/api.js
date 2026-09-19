const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function authHeaders() {
  const token = localStorage.getItem("access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `Request failed: ${res.status}`);
  }
  return res.status === 204 ? null : res.json();
}

export const api = {
  register: (email, password, full_name) =>
    request("/auth/register", { method: "POST", body: JSON.stringify({ email, password, full_name }) }),

  login: async (email, password) => {
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);
    const res = await fetch(`${API_URL}/auth/login`, { method: "POST", body: form });
    if (!res.ok) throw new Error("Login failed");
    const data = await res.json();
    localStorage.setItem("access_token", data.access_token);
    return data;
  },

  listExams: () => request("/exams"),
  createExam: (payload) => request("/exams", { method: "POST", body: JSON.stringify(payload) }),
  getExam: (id) => request(`/exams/${id}`),

  addTopics: (topics) => request("/syllabus/topics", { method: "POST", body: JSON.stringify(topics) }),
  listTopics: (subjectId) => request(`/syllabus/topics/${subjectId}`),

  generatePlan: (examId) => request(`/study-plan/${examId}/generate`, { method: "POST" }),
  getPlan: (examId) => request(`/study-plan/${examId}`),
  updateSessionStatus: (sessionId, status) =>
    request(`/study-plan/session/${sessionId}`, { method: "PATCH", body: JSON.stringify({ status }) }),

  generateQuiz: (topicId, numQuestions = 5) =>
    request("/quiz/generate", { method: "POST", body: JSON.stringify({ topic_id: topicId, num_questions: numQuestions }) }),
  submitQuiz: (topicId, answers) =>
    request("/quiz/submit", { method: "POST", body: JSON.stringify({ topic_id: topicId, answers }) }),

  getMastery: (examId) => request(`/progress/${examId}/mastery`),
  getReadiness: (examId) => request(`/progress/${examId}/readiness`),

  explainTopic: (topicId, level = "intermediate") =>
    request("/tutor/explain", { method: "POST", body: JSON.stringify({ topic_id: topicId, level }) }),
};
