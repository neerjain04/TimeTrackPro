// src/App.jsx
import React, { useState } from 'react';
import CategoryChart from './components/CategoryChart';
import DataTable from './components/DataTable';
import Timesheet from './pages/Timesheet';
import AnalyticsPanel from './components/AnalyticsPanel';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function formatDateInput(date) {
  return date.toISOString().slice(0, 10);
}

function App() {
  const [date, setDate] = useState(formatDateInput(new Date()));
  return (
    <Router>
      <div>
        {/* Top Nav */}
        <div className="header-bar">
          TimeTrackPro
        </div>
        <Routes>
          <Route path="/" element={
            <main className="dashboard-main dashboard-flex-row">
              <section className="dashboard-main-left">
                {/* Date Picker for dashboard analytics */}
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
                  <input
                    type="date"
                    value={date}
                    max={formatDateInput(new Date())}
                    onChange={e => setDate(e.target.value)}
                    style={{
                      padding: '0.5rem',
                      borderRadius: '4px',
                      border: '1px solid #ccc',
                      fontSize: '1rem',
                      marginLeft: 'auto',
                      marginRight: 0
                    }}
                  />
                </div>
                <CategoryChart date={date} />
                <DataTable date={date} />
              </section>
              <aside className="dashboard-analytics-right">
                <AnalyticsPanel date={date} />
              </aside>
            </main>
          } />
          <Route path="/timesheet" element={<Timesheet />} />
        </Routes>
        {/* Footer */}
        <footer className="dashboard-footer">
          © 2025 TimeTrackPro
        </footer>
      </div>
    </Router>
  );
}

export default App;