import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import CourseList from './pages/CourseList';
import CourseForm from './pages/CourseForm';
import RoomAllocationList from './pages/RoomAllocationList';
import RoomAllocationForm from './pages/RoomAllocationForm';
import StudentList from './pages/StudentList';
import StudentForm from './pages/StudentForm';
import StudentCourseList from './pages/StudentCourseList';
import StudentCourseForm from './pages/StudentCourseForm';

export default function App() {
  return (
    <Router>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <strong>Aayu App</strong> | <Link to='/course'>Course</Link> | <Link to='/room_allocation'>RoomAllocation</Link> | <Link to='/student'>Student</Link> | <Link to='/student_course'>StudentCourse</Link> 
      </nav>
      <div style={{ padding: '1rem' }}>
        <Routes>
          <Route path='/' element={<h2>Welcome to Aayu Generated App</h2>} />
          <Route path='/course' element={<CourseList />} />
          <Route path='/course/new' element={<CourseForm />} />
          <Route path='/course/edit/:id' element={<CourseForm />} />
          <Route path='/room_allocation' element={<RoomAllocationList />} />
          <Route path='/room_allocation/new' element={<RoomAllocationForm />} />
          <Route path='/room_allocation/edit/:id' element={<RoomAllocationForm />} />
          <Route path='/student' element={<StudentList />} />
          <Route path='/student/new' element={<StudentForm />} />
          <Route path='/student/edit/:id' element={<StudentForm />} />
          <Route path='/student_course' element={<StudentCourseList />} />
          <Route path='/student_course/new' element={<StudentCourseForm />} />
          <Route path='/student_course/edit/:id' element={<StudentCourseForm />} />
        </Routes>
      </div>
    </Router>
  );
}
