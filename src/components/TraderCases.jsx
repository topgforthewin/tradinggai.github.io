import { useEffect, useState } from "react";
import { api } from "../api";

export default function TraderCases() {
  const [cases, setCases] = useState([]);

  useEffect(() => {
    api.traders().then((d) => setCases(d.case_studies)).catch(() => {});
  }, []);

  return (
    <div>
      <div className="banner">
        These are historical case studies for context, not a playbook.
        Each of these traders had deep research and large capital behind a
        single bet - most people trying to copy the pattern don't have
        either, and most attempts at trades like these lose money.
      </div>
      {cases.map((c) => (
        <div className="card" key={c.name}>
          <p className="trader-name">{c.name}</p>
          <p className="trader-summary">{c.summary}</p>
        </div>
      ))}
    </div>
  );
}
