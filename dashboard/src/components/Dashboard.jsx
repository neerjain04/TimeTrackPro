import React, { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/usage")
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error("API error:", err));
  }, []);

  return (
    <div className="bg-white p-6 rounded-2xl shadow-md">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Time Usage Summary</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="Category" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="Duration (Minutes)" fill="#ef4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
