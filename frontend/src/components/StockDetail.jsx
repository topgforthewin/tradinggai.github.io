import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { api } from "../api";

export default function StockDetail({ ticker }) {
  const [chart, setChart] = useState(null);
  const [signal, setSignal] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!ticker) return;
    setChart(null);
    setSignal(null);
    setError(null);
    api.stockChart(ticker).then(setChart).catch((e) => setError(e.message));
    api.stockSignal(ticker).then(setSignal).catch(() => {});
  }, [ticker]);

  if (!ticker) {
    return <div className="card">Pick a stock from the watchlist to see its chart and signal.</div>;
  }
  if (error) return <div className="card">Couldn't load {ticker}: {error}</div>;
  if (!chart) return <div className="card">Loading {ticker}...</div>;

  const points = (chart.points || []).map((p) => ({
    date: p.timestamp ? new Date(p.timestamp).toLocaleDateString() : p.date,
    close: p.close ?? p.value,
  }));

  return (
    <div>
      <div className="card">
        <p className="stat-label">{ticker} - price history</p>
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={points}>
            <CartesianGrid stroke="#262b35" strokeDasharray="3 3" />
            <XAxis dataKey="date" hide />
            <YAxis domain={["auto", "auto"]} width={50} stroke="#9aa1ac" />
            <Tooltip
              contentStyle={{ background: "#171a21", border: "1px solid #262b35" }}
            />
            <Line type="monotone" dataKey="close" stroke="#5b8def" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {signal && (
        <div className="card">
          <p className="stat-label">Signal read</p>
          <span className={`badge ${signal.signal.label.split(" ")[0]}`}>
            {signal.signal.label}
          </span>
          <ul className="reasons">
            {signal.signal.reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
