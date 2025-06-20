import React, { useEffect, useState } from "react";
import "../global.css";

export default function Timesheet() {
  const [sessions, setSessions] = useState([]);
  const [view, setView] = useState("daily");
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/timesheet")
      .then(res => res.json())
      .then(data => setSessions(data))
      .catch(() => setError("Failed to fetch timesheet data"));
  }, []);

  // Calculate total hours for the period
  const totalHours = sessions.reduce((sum, s) => {
    const [h, m, s_] = s.duration.split(":").map(Number);
    return sum + h + m / 60 + s_ / 3600;
  }, 0).toFixed(1);

  // Navigation tabs
  const tabs = [
    { key: "daily", label: "Today" },
    { key: "weekly", label: "This Week" },
    { key: "monthly", label: "This Month" },
  ];

  return (
    <>
      <div className="container">
        <div className="section-title">Employee Timesheet</div>
        <div className="summary">
          <div className="summary-info">John Doe &bull; Software Engineer</div>
          <div className="summary-hours">{totalHours} hrs</div>
          <button className="button-primary">Add Time</button>
        </div>
        <div className="tabs">
          {tabs.map(tab => (
            <button
              key={tab.key}
              className={`tab${view === tab.key ? " active" : ""}`}
              onClick={() => setView(tab.key)}
              disabled={tab.key !== "daily"}
            >
              {tab.label}
            </button>
          ))}
        </div>
        <table className="timesheet-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Duration</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {sessions.map((s, idx) => (
              <tr key={idx}>
                <td>{s.type}</td>
                <td>{s.start_time}</td>
                <td>{s.end_time}</td>
                <td>{s.duration}</td>
                <td></td>
              </tr>
            ))}
          </tbody>
        </table>
        {error && <div style={{ color: "#ec1c24", padding: "2rem" }}>{error}</div>}
      </div>
    </>
  );
}