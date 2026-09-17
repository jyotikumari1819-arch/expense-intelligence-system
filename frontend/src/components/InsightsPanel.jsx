export default function InsightsPanel({ insight, total, count }) {
  return (
    <div className="insights-panel">
      <h3>AI Spending Insight</h3>
      <p className="insight-text">{insight || "Add some expenses to see AI-generated insights here."}</p>
      <div className="insight-stats">
        <span>Total: ₹{(total || 0).toFixed(2)}</span>
        <span>{count || 0} transactions</span>
      </div>
    </div>
  );
}
