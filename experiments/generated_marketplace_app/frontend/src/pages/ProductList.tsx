import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function ProductList() {
  const [items, setItems] = useState<any[]>([]);

  const fetchItems = async () => {
    const res = await api.get('/product');
    setItems(res.data);
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleDelete = async (id: string) => {
    await api.delete(`/product/${id}`);
    fetchItems();
  };

  return (
    <div>
      <h1>Product List</h1>
      <Link to="/product/new">
        <button>Add New Product</button>
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
                <Link to={`/product/edit/${item.id}`}>
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
