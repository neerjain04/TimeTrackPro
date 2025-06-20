import React, { useEffect, useState } from "react";
import "../global.css";

function exportCSV(sessions) {
  if (!sessions.length) return;
  const headers = ["Type", "Start Time", "End Time", "Duration"];
  const rows = sessions.map(s => [s.type, s.start_time, s.end_time, s.duration]);
  let csv = [headers.join(",")].concat(rows.map(r => r.join(","))).join("\r\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `timesheet_${new Date().toISOString().slice(0,10)}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function formatDateInput(date) {
  return date.toISOString().slice(0, 10);
}

function formatDateTimeLocalToCSV(dt) {
  if (!dt) return '';
  // Replace T with space, ensure seconds
  let [date, time] = dt.split('T');
  if (!time) return dt.replace('T', ' ');
  if (time.length === 5) time += ':00'; // HH:mm -> HH:mm:ss
  return `${date} ${time}`;
}

function EditModal({ open, onClose, session, onSave }) {
  const [type, setType] = useState(session?.type || "Work");
  const [start, setStart] = useState(session?.start_time || "");
  const [end, setEnd] = useState(session?.end_time || "");
  useEffect(() => {
    setType(session?.type || "Work");
    setStart(session?.start_time || "");
    setEnd(session?.end_time || "");
  }, [session]);
  if (!open) return null;
  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h3>Edit Session</h3>
        <label>Type: <select value={type} onChange={e => setType(e.target.value)}><option>Work</option><option>Meal</option><option>Idle</option></select></label>
        <label>Start Time: <input type="datetime-local" value={start} onChange={e => setStart(e.target.value)} /></label>
        <label>End Time: <input type="datetime-local" value={end} onChange={e => setEnd(e.target.value)} /></label>
        <div style={{marginTop: '1rem'}}>
          <button className="button-primary" onClick={() => onSave({ type, start_time: formatDateTimeLocalToCSV(start), end_time: formatDateTimeLocalToCSV(end) })}>Save</button>
          <button className="button-primary" style={{marginLeft: '1rem', background: '#b71c1c'}} onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
}

// Analytics helpers
function getLongestSession(sessions) {
  if (!sessions.length) return '-';
  let max = sessions[0];
  for (let s of sessions) {
    if (s.duration && s.duration > max.duration) max = s;
  }
  return max.duration || '-';
}
function getMostFrequentType(sessions) {
  if (!sessions.length) return '-';
  const counts = {};
  for (let s of sessions) counts[s.type] = (counts[s.type] || 0) + 1;
  let maxType = Object.keys(counts)[0];
  for (let t in counts) if (counts[t] > counts[maxType]) maxType = t;
  return maxType;
}
function getFirstEntry(sessions) {
  if (!sessions.length) return '-';
  let first = sessions[0];
  for (let s of sessions) if (s.start_time < first.start_time) first = s;
  return first.start_time;
}

export default function Timesheet() {
  const [sessions, setSessions] = useState([]);
  const [view, setView] = useState("daily");
  const [error, setError] = useState(null);
  const [tracking, setTracking] = useState(null);
  const [date, setDate] = useState(formatDateInput(new Date()));
  const [editIdx, setEditIdx] = useState(null);
  const [editSession, setEditSession] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetch(`/api/timesheet?date=${date}`)
      .then(res => res.json())
      .then(data => setSessions(data))
      .catch(() => setError("Failed to fetch timesheet data"));
  }, [date]);

  // Calculate total hours for the period
  const totalHours = sessions.reduce((sum, s) => {
    if (!s.duration) return sum;
    const [h, m, s_] = s.duration.split(":").map(Number);
    if ([h, m, s_].some(isNaN)) return sum;
    return sum + h + m / 60 + s_ / 3600;
  }, 0).toFixed(2);

  // Navigation tabs
  const tabs = [
    { key: "daily", label: "Today" },
    { key: "weekly", label: "This Week" },
    { key: "monthly", label: "This Month" },
  ];

  const handleStartTracking = async () => {
    setTracking('starting');
    const res = await fetch('/api/tracking/start', { method: 'POST' });
    const data = await res.json();
    setTracking(data.success ? 'on' : null);
  };

  const handleStopTracking = async () => {
    setTracking('stopping');
    const res = await fetch('/api/tracking/stop', { method: 'POST' });
    const data = await res.json();
    setTracking(data.success ? 'off' : null);
  };

  const handleEdit = (idx) => {
    setEditIdx(idx);
    setEditSession(sessions[idx]);
    setModalOpen(true);
  };
  const handleSaveEdit = async (newData) => {
    setModalOpen(false);
    if (editIdx == null) return;
    // Grouped edit (as before)
    const indices = sessions[editIdx]?.indices || [];
    const res = await fetch('/api/timesheet/edit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ indices, date, ...newData })
    });
    const data = await res.json();
    if (data.success) {
      fetch(`/api/timesheet?date=${date}`)
        .then(res => res.json())
        .then(data => setSessions(data));
    }
    setEditIdx(null);
    setEditSession(null);
  };

  return (
    <>
      <EditModal open={modalOpen} onClose={() => setModalOpen(false)} session={editSession} onSave={handleSaveEdit} />
      <div className="container">
        <div className="section-title">Employee Timesheet</div>
        <div className="summary-analytics-row">
          <div className="summary-card summary-left">
            <div className="summary-main">
              <div className="summary-hours-large">{totalHours} <span className="summary-hrs-label">hrs</span></div>
              <div className="summary-info-large">John Doe &bull; Software Engineer</div>
            </div>
          </div>
          <div className="analytics-card summary-right">
            <div className="analytics-title">Analytics</div>
            <div className="analytics-item"><b>Longest Session:</b> {getLongestSession(sessions)}</div>
            <div className="analytics-item"><b>Most Frequent Type:</b> {getMostFrequentType(sessions)}</div>
            <div className="analytics-item"><b>First Entry:</b> {getFirstEntry(sessions)}</div>
            {/* Add more analytics as needed */}
          </div>
        </div>
        <div className="summary">
          <button className="button-primary button-wide">Add Time</button>
          <button className="button-primary button-wide" style={{marginLeft: '1rem', background: tracking === 'on' ? '#43a047' : undefined}} onClick={handleStartTracking} disabled={tracking === 'on' || tracking === 'starting'}>
            {tracking === 'starting' ? 'Starting...' : 'Start Time Tracking'}
          </button>
          <button className="button-primary button-wide" style={{marginLeft: '0.5rem', background: tracking === 'off' ? '#b71c1c' : undefined}} onClick={handleStopTracking} disabled={tracking === 'off' || tracking === 'stopping'}>
            {tracking === 'stopping' ? 'Stopping...' : 'Stop Time Tracking'}
          </button>
          <button className="button-primary button-wide" style={{marginLeft: '1rem', background: '#ec1c24', color: 'white'}} onClick={() => exportCSV(sessions)}>
            Export as CSV
          </button>
          <input type="date" value={date} max={formatDateInput(new Date())} onChange={e => setDate(e.target.value)} style={{marginLeft: '1rem', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc'}} />
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
                <td><button className="button-primary" style={{padding: '0.2rem 0.5rem', fontSize: '0.9em'}} onClick={() => handleEdit(idx)}>Edit</button></td>
              </tr>
            ))}
          </tbody>
        </table>
        {error && <div style={{ color: "#ec1c24", padding: "2rem" }}>{error}</div>}
      </div>
    </>
  );
}