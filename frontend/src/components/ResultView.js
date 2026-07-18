// Renders structured AI output (summary, risks, actions) with defensive handling for inconsistent model responses
// Displays processed results while safely handling malformed or unexpected data formats
function ResultView({ result }) {
  // Prevent rendering if result is not yet available
  if (!result) return null;

  // Ensure summary is always rendered as string (handles unexpected object responses from model)
  const summaryText =
    typeof result.summary?.summary === "string"
      ? result.summary.summary
      : JSON.stringify(result.summary?.summary || "");

  return (
    <div className="result">

      {/* Displays AI-generated clinical summary */}
      <div className="card">
        <h3>Summary</h3>
        <p>{summaryText}</p>
      </div>

      {/* Renders detected risks with severity-based styling */}
      <div className="card">
        <h3>Risks</h3>
        <ul>
          {Array.isArray(result.summary?.risks) &&
            result.summary.risks.map((r, i) => {
              // Normalize risk fields to strings to prevent React rendering errors
              const type =
                typeof r?.type === "string"
                  ? r.type
                  : JSON.stringify(r?.type || "");

              const severity =
                typeof r?.severity === "string"
                  ? r.severity
                  : JSON.stringify(r?.severity || "");

              return (
                <li key={i} className={`risk-${severity.toLowerCase()}`}>
                  ⚠️ <strong>{type}</strong> — {severity}
                </li>
              );
            })}
        </ul>
      </div>

      {/* Displays recommended actions with fallback handling for structured or raw outputs */}
      <div className="card">
        <h3>Actions</h3>
        <ul>
          {Array.isArray(result.summary?.actions) &&
            result.summary.actions.map((a, i) => {
              // Supports both string and object-based action formats from model
              const actionText =
                typeof a === "string"
                  ? a
                  : typeof a?.action === "string"
                  ? `${a.action} (${a.priority || "normal"})`
                  : JSON.stringify(a);

              return <li key={i}>{actionText}</li>;
            })}
        </ul>
      </div>

    </div>
  );
}