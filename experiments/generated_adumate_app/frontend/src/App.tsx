import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import CourseList from './pages/CourseList';
import CourseForm from './pages/CourseForm';
import RoomAllocationList from './pages/RoomAllocationList';
import RoomAllocationForm from './pages/RoomAllocationForm';
import StudentList from './pages/StudentList';
import StudentForm from './pages/StudentForm';
import StudentCourseList from './pages/StudentCourseList';
import StudentCourseForm from './pages/StudentCourseForm';

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
        <Link to="/course" style={{marginRight: "1rem"}}>Course</Link>
        <Link to="/room_allocation" style={{marginRight: "1rem"}}>Room Allocation</Link>
        <Link to="/student" style={{marginRight: "1rem"}}>Student</Link>
        <Link to="/student_course" style={{marginRight: "1rem"}}>Student Course</Link>
      </nav>
      <div style={{ padding: '0 2rem' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/course" element={<CourseList />} />
          <Route path="/course/new" element={<CourseForm />} />
          <Route path="/course/edit/:id" element={<CourseForm />} />
          <Route path="/room_allocation" element={<RoomAllocationList />} />
          <Route path="/room_allocation/new" element={<RoomAllocationForm />} />
          <Route path="/room_allocation/edit/:id" element={<RoomAllocationForm />} />
          <Route path="/student" element={<StudentList />} />
          <Route path="/student/new" element={<StudentForm />} />
          <Route path="/student/edit/:id" element={<StudentForm />} />
          <Route path="/student_course" element={<StudentCourseList />} />
          <Route path="/student_course/new" element={<StudentCourseForm />} />
          <Route path="/student_course/edit/:id" element={<StudentCourseForm />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
