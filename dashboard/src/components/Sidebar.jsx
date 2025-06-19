import React from "react";

export default function Sidebar() {
  return (
    <div className="w-64 bg-white shadow-lg p-4">
      <h2 className="text-xl font-semibold text-red-500 mb-4">TimeTrackPro</h2>
      <ul className="space-y-2">
        <li className="text-gray-700 hover:text-red-600 cursor-pointer">Dashboard</li>
        <li className="text-gray-700 hover:text-red-600 cursor-pointer">Reports</li>
        <li className="text-gray-700 hover:text-red-600 cursor-pointer">Settings</li>
      </ul>
    </div>
  );
}
