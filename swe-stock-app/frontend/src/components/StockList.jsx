import { useEffect, useState } from "react";
import { api } from "../api";

export default function StockList({ onSelect }) {
  const [tickers, setTickers] = useState([]);

  useEffect(() => {
    api.watchlist().then((d) => setTickers(d.tickers)).catch(() => {});
  }, []);

  return (
    <div className="card">
      <p className="stat-label">OMXS30 watchlist</p>
      {tickers.map((t) => (
        <div className="list-row" key={t.ticker} onClick={() => onSelect(t.ticker)}>
          <span>{t.name}</span>
          <span style={{ color: "var(--text-muted)" }}>{t.ticker}</span>
        </div>
      ))}
    </div>
  );
}
