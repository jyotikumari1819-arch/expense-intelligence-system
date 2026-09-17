const BASE_URL = "http://localhost:8000";

function authHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function handle(res) {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  signup: (data) =>
    fetch(`${BASE_URL}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then(handle),

  login: (data) =>
    fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then(handle),

  forgotPassword: (data) =>
    fetch(`${BASE_URL}/auth/forgot-password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then(handle),

  resetPassword: (data) =>
    fetch(`${BASE_URL}/auth/reset-password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then(handle),

  getExpenses: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return fetch(`${BASE_URL}/expenses${qs ? `?${qs}` : ""}`, {
      headers: authHeaders(),
    }).then(handle);
  },

  createExpense: (data) =>
    fetch(`${BASE_URL}/expenses`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify(data),
    }).then(handle),

  deleteExpense: (id) =>
    fetch(`${BASE_URL}/expenses/${id}`, {
      method: "DELETE",
      headers: authHeaders(),
    }).then(handle),

  getCategories: () =>
    fetch(`${BASE_URL}/categories`, { headers: authHeaders() }).then(handle),

  getMonthlyInsight: (month, year) => {
    const qs = new URLSearchParams({ month, year }).toString();
    return fetch(`${BASE_URL}/insights/monthly?${qs}`, {
      headers: authHeaders(),
    }).then(handle);
  },
};
