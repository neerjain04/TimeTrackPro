// src/App.jsx
import React from 'react';
import CategoryChart from './components/CategoryChart';
import DataTable from './components/DataTable';
import Timesheet from './pages/Timesheet';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-white text-gray-900 font-sans">
        {/* Top Nav */}
        <nav className="bg-[#ec1c24]">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center">
            <span className="text-white text-2xl font-bold tracking-tight font-sans">TimeTrackPro</span>
          </div>
        </nav>
        <Routes>
          <Route path="/" element={
            <main className="w-full max-w-7xl mx-auto px-6 py-12 space-y-12">
              <section>
                <CategoryChart />
              </section>
              <section>
                <DataTable />
              </section>
            </main>
          } />
          <Route path="/timesheet" element={<Timesheet />} />
        </Routes>
        {/* Footer */}
        <footer className="bg-gray-100 text-gray-500 text-center text-sm py-4">
          © 2025 TimeTrackPro
        </footer>
      </div>
    </Router>
  );
}

export default App;