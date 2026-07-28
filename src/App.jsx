import { useState } from "react";
import Portfolio from "./components/Portfolio.jsx";
import StockList from "./components/StockList.jsx";
import StockDetail from "./components/StockDetail.jsx";
import TraderCases from "./components/TraderCases.jsx";

const TABS = ["Portfolio", "Screener", "Trader case studies"];

export default function App() {
  const [tab, setTab] = useState("Portfolio");
  const [selectedTicker, setSelectedTicker] = useState(null);

  return (
    <div className="app">
      <div className="header">
        <h1>Swedish stock research dashboard</h1>
        <p>Read-only portfolio view and technical screener for the Stockholm exchange. Not investment advice.</p>
      </div>

      <div className="banner">
        This app is read-only: it never places, edits, or cancels orders on your
        Avanza account. The technical signals below describe recent price
        behavior - they are not predictions and are not a guarantee of profit.
      </div>

      <div className="tabs">
        {TABS.map((t) => (
          <button key={t} className={tab === t ? "active" : ""} onClick={() => setTab(t)}>
            {t}
          </button>
        ))}
      </div>

      {tab === "Portfolio" && <Portfolio />}

      {tab === "Screener" && (
        <div className="grid" style={{ gridTemplateColumns: "280px 1fr" }}>
          <StockList onSelect={setSelectedTicker} />
          <StockDetail ticker={selectedTicker} />
        </div>
      )}

      {tab === "Trader case studies" && <TraderCases />}
    </div>
  );
}
