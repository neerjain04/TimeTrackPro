// src/components/DataTable.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import "../global.css";

function DataTable({ date }) {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios
      .get(`http://localhost:5000/api/data?date=${date}`)
      .then((response) => setLogs(response.data))
      .catch((error) => console.error("Error fetching data:", error));
  }, [date]);

  return (
    <div className="dashboard-card">
      <h2 className="dashboard-title">App Usage Log</h2>
      <div style={{ overflowX: "auto" }}>
        <table className="dashboard-table">
          <thead>
            <tr>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Duration</th>
              <th>Window Title</th>
              <th>Category</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log, index) => (
              <tr key={index}>
                <td>{log["Start Time"]}</td>
                <td>{log["End Time"]}</td>
                <td>{log["Duration"]}</td>
                <td>{log["Window Title"]}</td>
                <td>{log["Category"]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DataTable;
