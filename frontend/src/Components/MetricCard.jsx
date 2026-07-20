// MetricCard.jsx
// WHAT: A small, reusable card component showing one fairness number,
// color-coded green/red based on whether it passes a fairness threshold.

export default function MetricCard({ label, value, isGood, description }) {
    return (
        <div className={`metric-card ${isGood ? "good" : "bad"}`}>
            <div className="metric-label">{label}</div>
            <div className="metric-value">{value}</div>
            <div className="metric-description">{description}</div>
        </div>
    );
}

