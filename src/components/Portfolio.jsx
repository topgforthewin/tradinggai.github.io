import { useEffect, useState } from "react";
import { api } from "../api";

export default function Portfolio() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.portfolio().then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) return <div className="card">Couldn't load portfolio: {error}</div>;
  if (!data) return <div className="card">Loading portfolio...</div>;

  const accounts = data.overview?.accounts || [];
  const positions =
    data.positions?.instrumentPositions?.flatMap((g) => g.positions) || [];

  return (
    <div>
      <div className="grid">
        {accounts.map((acc) => (
          <div className="card" key={acc.accountId}>
            <p className="stat-label">{acc.name}</p>
            <p className="stat-value">
              {acc.totalValue?.toLocaleString("sv-SE")} kr
            </p>
            <p className={acc.totalProfit >= 0 ? "up" : "down"}>
              {acc.totalProfit >= 0 ? "+" : ""}
              {acc.totalProfit?.toLocaleString("sv-SE")} kr (
              {acc.totalProfitPercent}%)
            </p>
          </div>
        ))}
      </div>

      <div className="card">
        <p className="stat-label">Holdings</p>
        {positions.map((p, i) => (
          <div className="list-row" key={i}>
            <span>{p.name} ({p.ticker})</span>
            <span>
              {p.volume} sh @ {p.lastPrice} kr
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
