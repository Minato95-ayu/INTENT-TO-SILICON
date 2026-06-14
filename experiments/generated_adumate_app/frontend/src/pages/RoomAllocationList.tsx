import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function RoomAllocationList() {
  const [items, setItems] = useState<any[]>([]);

  const fetchItems = async () => {
    const res = await api.get('/room_allocation');
    setItems(res.data);
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleDelete = async (id: string) => {
    await api.delete(`/room_allocation/${id}`);
    fetchItems();
  };

  return (
    <div>
      <h1>RoomAllocation List</h1>
      <Link to="/room_allocation/new">
        <button>Add New RoomAllocation</button>
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
                <Link to={`/room_allocation/edit/${item.id}`}>
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
