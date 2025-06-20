import React, { useEffect, useState } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";
import "../global.css";

const COLORS = ["#ec1c24", "#f9a825", "#43a047", "#1976d2", "#8e24aa", "#ff7043", "#789262"];

export default function CategoryPie() {
  const [data, setData] = useState([]);
  useEffect(() => {
    axios
      .get("http://localhost:5000/api/usage")
      .then((response) => setData(response.data))
      .catch((error) => console.error("Pie API Error:", error));
  }, []);
  return (
    <div className="analytics-pie">
      <h3 style={{ color: "#ec1c24", marginBottom: "1rem", textAlign: "center" }}>Category Breakdown</h3>
      <ResponsiveContainer width="100%" height={220}>
        <PieChart>
          <Pie
            data={data}
            dataKey="Duration (Minutes)"
            nameKey="Category"
            cx="50%"
            cy="50%"
            outerRadius={80}
            fill="#ec1c24"
            label={({ name }) => name}
          >
            {data.map((entry, idx) => (
              <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(v) => `${v} min`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
