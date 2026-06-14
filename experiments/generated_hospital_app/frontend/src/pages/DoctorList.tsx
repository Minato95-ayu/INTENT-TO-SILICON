import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function DoctorList() {
  const [items, setItems] = useState<any[]>([]);

  const fetchItems = async () => {
    const res = await api.get('/doctor');
    setItems(res.data);
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleDelete = async (id: string) => {
    await api.delete(`/doctor/${id}`);
    fetchItems();
  };

  return (
    <div>
      <h1>Doctor List</h1>
      <Link to="/doctor/new">
        <button>Add New Doctor</button>
      </Link>
      <table border={1} style={{ marginTop: "1rem" }}>
        <thead>
          <tr>
            <th>ID</th>
            
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              
              <td>
                <Link to={`/doctor/edit/${item.id}`}>
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
