import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import AppointmentList from './pages/AppointmentList';
import AppointmentForm from './pages/AppointmentForm';
import DoctorList from './pages/DoctorList';
import DoctorForm from './pages/DoctorForm';
import PatientList from './pages/PatientList';
import PatientForm from './pages/PatientForm';

export default function App() {
  return (
    <Router>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <strong>Aayu App</strong> | <Link to='/appointment'>Appointment</Link> | <Link to='/doctor'>Doctor</Link> | <Link to='/patient'>Patient</Link> 
      </nav>
      <div style={{ padding: '1rem' }}>
        <Routes>
          <Route path='/' element={<h2>Welcome to Aayu Generated App</h2>} />
          <Route path='/appointment' element={<AppointmentList />} />
          <Route path='/appointment/new' element={<AppointmentForm />} />
          <Route path='/appointment/edit/:id' element={<AppointmentForm />} />
          <Route path='/doctor' element={<DoctorList />} />
          <Route path='/doctor/new' element={<DoctorForm />} />
          <Route path='/doctor/edit/:id' element={<DoctorForm />} />
          <Route path='/patient' element={<PatientList />} />
          <Route path='/patient/new' element={<PatientForm />} />
          <Route path='/patient/edit/:id' element={<PatientForm />} />
        </Routes>
      </div>
    </Router>
  );
}
