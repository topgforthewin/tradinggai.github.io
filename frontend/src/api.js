const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function get(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  health: () => get("/api/health"),
  portfolio: () => get("/api/portfolio"),
  watchlist: () => get("/api/watchlist"),
  stockChart: (ticker, period = "one_year") =>
    get(`/api/stock/${ticker}/chart?period=${period}`),
  stockSignal: (ticker, period = "one_year") =>
    get(`/api/stock/${ticker}/signal?period=${period}`),
  traders: () => get("/api/traders"),
};
