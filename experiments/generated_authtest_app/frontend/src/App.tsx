import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import AppointmentList from './pages/AppointmentList';
import AppointmentForm from './pages/AppointmentForm';
import AuthList from './pages/AuthList';
import AuthForm from './pages/AuthForm';
import PatientList from './pages/PatientList';
import PatientForm from './pages/PatientForm';
import RoleList from './pages/RoleList';
import RoleForm from './pages/RoleForm';
import UserList from './pages/UserList';
import UserForm from './pages/UserForm';
import Login from './pages/Login';
import Register from './pages/Register';

export default function App() {
  return (
    <Router>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <strong>Aayu App</strong> | <Link to='/appointment'>Appointment</Link> | <Link to='/auth'>Auth</Link> | <Link to='/patient'>Patient</Link> | <Link to='/role'>Role</Link> | <Link to='/user'>User</Link> 
        <div style={{ float: 'right' }}>
          <Link to="/login">Login</Link> | <Link to="/register">Register</Link> | 
          <button onClick={() => { localStorage.removeItem('token'); window.location.href='/login'; }}>Logout</button>
        </div>
      </nav>
      <div style={{ padding: '1rem' }}>
        <Routes>
          <Route path='/' element={<h2>Welcome to Aayu Generated App</h2>} />
          <Route path='/login' element={<Login />} />
          <Route path='/register' element={<Register />} />
          <Route path='/appointment' element={<AppointmentList />} />
          <Route path='/appointment/new' element={<AppointmentForm />} />
          <Route path='/appointment/edit/:id' element={<AppointmentForm />} />
          <Route path='/auth' element={<AuthList />} />
          <Route path='/auth/new' element={<AuthForm />} />
          <Route path='/auth/edit/:id' element={<AuthForm />} />
          <Route path='/patient' element={<PatientList />} />
          <Route path='/patient/new' element={<PatientForm />} />
          <Route path='/patient/edit/:id' element={<PatientForm />} />
          <Route path='/role' element={<RoleList />} />
          <Route path='/role/new' element={<RoleForm />} />
          <Route path='/role/edit/:id' element={<RoleForm />} />
          <Route path='/user' element={<UserList />} />
          <Route path='/user/new' element={<UserForm />} />
          <Route path='/user/edit/:id' element={<UserForm />} />
        </Routes>
      </div>
    </Router>
  );
}
