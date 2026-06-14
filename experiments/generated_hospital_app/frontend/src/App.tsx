import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import DoctorList from './pages/DoctorList';
import DoctorForm from './pages/DoctorForm';
import PatientList from './pages/PatientList';
import PatientForm from './pages/PatientForm';

function Home() {
  return (
    <div>
      <h1>Aayu Generated Dashboard</h1>
      <p>Welcome to your full-stack application.</p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: '1rem', background: '#f0f0f0', marginBottom: '2rem' }}>
        <Link to="/" style={{marginRight: "2rem", fontWeight: "bold"}}>Home</Link>
        <Link to="/doctor" style={{marginRight: "1rem"}}>Doctor</Link>
        <Link to="/patient" style={{marginRight: "1rem"}}>Patient</Link>
      </nav>
      <div style={{ padding: '0 2rem' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/doctor" element={<DoctorList />} />
          <Route path="/doctor/new" element={<DoctorForm />} />
          <Route path="/doctor/edit/:id" element={<DoctorForm />} />
          <Route path="/patient" element={<PatientList />} />
          <Route path="/patient/new" element={<PatientForm />} />
          <Route path="/patient/edit/:id" element={<PatientForm />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
