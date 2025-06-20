// src/components/CategoryChart.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import "../global.css";

export default function CategoryChart({ date }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get(`http://localhost:5000/api/usage?date=${date}`)
      .then((response) => setData(response.data))
      .catch((error) => console.error("Chart API Error:", error));
  }, [date]);

  return (
    <div className="dashboard-card">
      <h2 className="dashboard-title">Time Spent by Category</h2>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data} barSize={40}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Category" stroke="#4B5563" fontSize={14} />
          <YAxis stroke="#4B5563" fontSize={14} />
          <Tooltip
            contentStyle={{ backgroundColor: "#fff", borderRadius: "6px", border: "1px solid #ccc" }}
          />
          <Bar
            dataKey="Duration (Minutes)"
            fill="#ec1c24"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
