// src/components/DataTable.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

function DataTable() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/data")
      .then((response) => setLogs(response.data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="bg-white shadow-md rounded-2xl border border-gray-200 p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4 tracking-tight">
        App Usage Log
      </h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 text-sm text-gray-700">
          <thead className="bg-gray-50 text-left text-gray-600 font-semibold uppercase text-xs">
            <tr>
              <th className="px-4 py-2">Start Time</th>
              <th className="px-4 py-2">End Time</th>
              <th className="px-4 py-2">Duration</th>
              <th className="px-4 py-2">Window Title</th>
              <th className="px-4 py-2">Category</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {logs.map((log, index) => (
              <tr
                key={index}
                className="hover:bg-gray-50 transition duration-150 ease-in-out"
              >
                <td className="px-4 py-2 whitespace-nowrap">{log["Start Time"]}</td>
                <td className="px-4 py-2 whitespace-nowrap">{log["End Time"]}</td>
                <td className="px-4 py-2 whitespace-nowrap">{log["Duration"]}</td>
                <td className="px-4 py-2">{log["Window Title"]}</td>
                <td className="px-4 py-2 font-medium">{log["Category"]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DataTable;
