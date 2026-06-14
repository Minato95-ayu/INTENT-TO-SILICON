import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function StudentCourseList() {
  const [items, setItems] = useState<any[]>([]);

  const fetchItems = async () => {
    const res = await api.get('/student_course');
    setItems(res.data);
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleDelete = async (id: string) => {
    await api.delete(`/student_course/${id}`);
    fetchItems();
  };

  return (
    <div>
      <h1>StudentCourse List</h1>
      <Link to="/student_course/new">
        <button>Add New StudentCourse</button>
      </Link>
      <table border={1} style={{ marginTop: "1rem" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Student_Id</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.student_id}</td>
              <td>
                <Link to={`/student_course/edit/${item.id}`}>
                  <button>Edit</button>
                </Link>
                <button onClick={() => handleDelete(item.id)} style={{ marginLeft: "0.5rem" }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
