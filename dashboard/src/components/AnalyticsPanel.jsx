import React, { useEffect, useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer } from "recharts";
import "../global.css";

export default function AnalyticsPanel({ date }) {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    axios.get(`http://localhost:5000/api/data?date=${date}`)
      .then(res => setLogs(res.data))
      .catch(() => setLogs([]));
  }, [date]);

  // Analytics calculations
  const totalHours = logs.reduce((sum, l) => {
    if (!l["Duration"]) return sum;
    const match = l["Duration"].match(/(\d+) days (\d+):(\d+):(\d+)/);
    if (match) {
      const [, d, h, m, s] = match.map(Number);
      return sum + d*24 + h + m/60 + s/3600;
    }
    return sum;
  }, 0).toFixed(2);

  const appCounts = {};
  logs.forEach(l => {
    const app = l["Window Title"];
    if (app) appCounts[app] = (appCounts[app] || 0) + 1;
  });
  const mostUsedApp = Object.keys(appCounts).reduce((a, b) => appCounts[a] > appCounts[b] ? a : b, "-");

  let longest = null, avg = 0;
  const sessionDurations = [];
  logs.forEach(l => {
    const match = l["Duration"]?.match(/(\d+) days (\d+):(\d+):(\d+)/);
    if (match) {
      const [, d, h, m, s] = match.map(Number);
      const total = d*24*60 + h*60 + m + s/60;
      sessionDurations.push({ name: l["Window Title"] || '', value: total });
      if (!longest || total > longest.total) longest = { ...l, total };
      avg += total;
    }
  });
  avg = logs.length ? (avg / logs.length).toFixed(1) : "-";

  const first = logs[0]?.["Start Time"] || "-";
  const last = logs[logs.length-1]?.["End Time"] || "-";

  return (
    <div className="dashboard-analytics-right">
      <div className="analytics-metric-group">
        <div className="metric-label">Total Hours</div>
        <div className="metric-value">{totalHours}</div>
        <div className="metric-divider" />
        <div className="metric-label">Most Used App</div>
        <div className="metric-value">{mostUsedApp}</div>
        <div className="metric-divider" />
        <div className="metric-label">Longest Session</div>
        <div className="metric-value">{longest ? longest["Duration"] : "-"}</div>
        <div className="metric-divider" />
        <div className="metric-label">Average Session (min)</div>
        <div className="metric-value">{avg}</div>
        <div className="metric-divider" />
        <div className="metric-label">First Entry</div>
        <div className="metric-value">{first}</div>
        <div className="metric-divider" />
        <div className="metric-label">Last Entry</div>
        <div className="metric-value">{last}</div>
        <div className="analytics-spark">
          <ResponsiveContainer width="100%" height={60}>
            <BarChart data={sessionDurations} margin={{ left: 20, right: 20, top: 0, bottom: 0 }}>
              <XAxis dataKey="name" hide />
              <Tooltip formatter={v => `${v.toFixed(1)} min`} />
              <Bar dataKey="value" fill="#ec1c24" radius={[4, 4, 0, 0]} barSize={12} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
