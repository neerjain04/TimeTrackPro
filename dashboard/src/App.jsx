// src/App.jsx
import React from 'react';
import CategoryChart from './components/CategoryChart';
import DataTable from './components/DataTable';
import Timesheet from './pages/Timesheet';
import AnalyticsPanel from './components/AnalyticsPanel';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
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
                <CategoryChart />
                <DataTable />
              </section>
              <aside className="dashboard-analytics-right">
                <AnalyticsPanel />
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