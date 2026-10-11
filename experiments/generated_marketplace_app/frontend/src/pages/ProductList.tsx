import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function ProductList() {
  const [items, setItems] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const size = 20;

  const fetchItems = async () => {
    const params = new URLSearchParams();
    params.append('page', page.toString());
    params.append('size', size.toString());
    if (search) params.append('search', search);
    
    const res = await api.get(`/product?${params.toString()}`);
    setItems(res.data.items || []);
  };

  useEffect(() => {
    fetchItems();
  }, [page]); // Re-fetch when page changes
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1); // Reset to first page on new search
    fetchItems();
  };

  const handleDelete = async (id: string) => {
    await api.delete(`/product/${id}`);
    fetchItems();
  };

  return (
    <div>
      <h1>Product List</h1>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <Link to="/product/new">
          <button>Add New Product</button>
        </Link>
        <form onSubmit={handleSearch}>
          <input 
            type="text" 
            placeholder="Search..." 
            value={search} 
            onChange={e => setSearch(e.target.value)} 
          />
          <button type="submit" style={{ marginLeft: '0.5rem' }}>Search</button>
        </form>
      </div>
      <table border={1} width="100%">
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
          {items.length === 0 && (
            <tr>
              <td colSpan={3} style={{ textAlign: 'center' }}>No records found.</td>
            </tr>
          )}
        </tbody>
      </table>
      
      <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Previous</button>
        <span>Page {page}</span>
        <button onClick={() => setPage(p => p + 1)}>Next</button>
      </div>
    </div>
  );
}
