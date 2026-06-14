import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function ProductOrderList() {
  const [items, setItems] = useState<any[]>([]);

  const fetchItems = async () => {
    const res = await api.get('/product_order');
    setItems(res.data);
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleDelete = async (id: string) => {
    await api.delete(`/product_order/${id}`);
    fetchItems();
  };

  return (
    <div>
      <h1>ProductOrder List</h1>
      <Link to="/product_order/new">
        <button>Add New ProductOrder</button>
      </Link>
      <table border={1} style={{ marginTop: "1rem" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Product_Id</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.product_id}</td>
              <td>
                <Link to={`/product_order/edit/${item.id}`}>
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
