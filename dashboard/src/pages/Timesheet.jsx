import React, { useEffect, useState } from "react";
import { Clock, Plus, Calendar, User } from "lucide-react";

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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center">
                <Clock className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Time Tracker</h1>
                <p className="text-gray-600">State Farm Employee Portal</p>
              </div>
            </div>
            <button className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center space-x-2 transition-colors">
              <Plus className="w-5 h-5" />
              <span>Clock In</span>
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Employee Info & Summary */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
                <User className="w-8 h-8 text-gray-600" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-gray-900">John Doe</h2>
                <p className="text-gray-600">Software Engineer</p>
                <p className="text-sm text-gray-500">Employee ID: SF001234</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-red-600">{totalHours}</div>
              <div className="text-gray-600 font-medium">Hours Today</div>
              <div className="text-sm text-gray-500 mt-1">Target: 8.0 hours</div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="mb-8">
          <div className="flex space-x-1">
            {tabs.map(tab => (
              <button
                key={tab.key}
                className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                  view === tab.key 
                    ? 'bg-red-600 text-white shadow-sm' 
                    : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
                }`}
                onClick={() => setView(tab.key)}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Time Entries */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="px-8 py-6 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Calendar className="w-5 h-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">
                {new Date().toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </h3>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left py-4 px-8 font-semibold text-gray-700">Activity</th>
                  <th className="text-left py-4 px-8 font-semibold text-gray-700">Start Time</th>
                  <th className="text-left py-4 px-8 font-semibold text-gray-700">End Time</th>
                  <th className="text-left py-4 px-8 font-semibold text-gray-700">Duration</th>
                  <th className="text-left py-4 px-8 font-semibold text-gray-700">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {sessions.map((session, idx) => (
                  <tr key={idx} className="hover:bg-gray-50 transition-colors">
                    <td className="py-6 px-8">
                      <div className="flex items-center space-x-3">
                        <div className={`w-3 h-3 rounded-full ${
                          session.type === 'Work' ? 'bg-red-600' : 'bg-yellow-500'
                        }`} />
                        <span className="font-medium text-gray-900">{session.type}</span>
                      </div>
                    </td>
                    <td className="py-6 px-8 text-gray-700">{session.start_time}</td>
                    <td className="py-6 px-8 text-gray-700">{session.end_time}</td>
                    <td className="py-6 px-8">
                      <span className="font-medium text-gray-900">{session.duration}</span>
                    </td>
                    <td className="py-6 px-8">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                        Complete
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {sessions.length === 0 && (
            <div className="text-center py-12">
              <Clock className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No time entries yet</h3>
              <p className="text-gray-600">Click "Clock In" to start tracking your time</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>State Farm Employee Time Tracking System</p>
        </div>
      </div>
    </div>
  );
}