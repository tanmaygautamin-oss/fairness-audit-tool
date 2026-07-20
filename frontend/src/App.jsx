// App.jsx
// WHAT: The main dashboard -- lets the user pick a sensitive attribute,
// run the audit, view results, and run mitigation, all interactively.
import { useState } from "react";
import { runAudit, runMitigation } from "./api";
import MetricCard from "./components/MetricCard";
import GroupChart from "./components/GroupChart";
import "./App.css";
export default function App() {
  const [attribute, setAttribute] = useState("sex");
  const [auditResult, setAuditResult] = useState(null);
  const [mitigationResult, setMitigationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  async function handleRunAudit() {
    setLoading(true);
    setMitigationResult(null);
    const result = await runAudit(attribute);
    setAuditResult(result);
    setLoading(false);
  }
  async function handleRunMitigation() {
    setLoading(true);
    const result = await runMitigation(attribute);
    setMitigationResult(result);
    setLoading(false);
  }
  return (
    <div className="dashboard">
      <header>
        <h1>⚖ Bias / Fairness Audit Dashboard</h1>
        <p>Auditing a real income-prediction model trained on real U.S. Census data.</p>
      </header>
      <div className="controls">
        <label>Audit fairness by:</label>
        <select value={attribute} onChange={(e) => setAttribute(e.target.value)}>
          <option value="sex">Sex</option>
          <option value="race">Race</option>
        </select>
        <button onClick={handleRunAudit} disabled={loading}>
          {loading ? "Running..." : "Run Fairness Audit"}
        </button>
      </div>
      {auditResult && (
        <>
          <section className="metrics-grid">
            <MetricCard
              label="Overall Accuracy"
              value={`${(auditResult.overall_fairness.overall_accuracy * 100).toFixed(1)}%`}
              isGood={true}
              description="How often the model is correct overall"
            />
            <MetricCard
              label="Disparate Impact Ratio"
              value={auditResult.overall_fairness.demographic_parity_ratio.toFixed(2)}
              isGood={auditResult.overall_fairness.demographic_parity_ratio >= 0.8}
              description="Should be ≥ 0.80 (the common '80% rule')"
            />
            <MetricCard
              label="Equalized Odds Gap"
              value={auditResult.overall_fairness.equalized_odds_difference.toFixed(3)}
              isGood={auditResult.overall_fairness.equalized_odds_difference <= 0.1}
              description="Should be ≤ 0.10 (lower is fairer)"
            />
          </section>
          <section className="charts-grid">
            <GroupChart perGroupData={auditResult.per_group} metricKey="selection_rate" title="Selection Rate by Group" />
            <GroupChart perGroupData={auditResult.per_group} metricKey="true_positive_rate" title="True Positive Rate by Group" />
          </section>
          <section className="flags">
            <h3>Audit Findings</h3>
            <ul>
              {auditResult.flags.map((flag, i) => <li key={i}>{flag}</li>)}
            </ul>
            <button onClick={handleRunMitigation} disabled={loading} className="mitigate-btn">
              {loading ? "Working..." : "Apply Bias Mitigation"}
            </button>
          </section>
        </>
      )}
      {mitigationResult && (
        <section className="mitigation-results">
          <h3>Before vs. After Mitigation</h3>
          <table>
            <thead><tr><th>Metric</th><th>Before</th><th>After</th></tr></thead>
            <tbody>
              <tr>
                <td>Accuracy</td>
                <td>{(auditResult.overall_fairness.overall_accuracy * 100).toFixed(1)}%</td>
                <td>{(mitigationResult.mitigated_accuracy * 100).toFixed(1)}%</td>
              </tr>
              <tr>
                <td>Equalized Odds Gap</td>
                <td>{auditResult.overall_fairness.equalized_odds_difference.toFixed(3)}</td>
                <td>{mitigationResult.mitigated_equalized_odds_difference.toFixed(3)}</td>
              </tr>
            </tbody>
          </table>
        </section>
      )}
    </div>
  );
}
