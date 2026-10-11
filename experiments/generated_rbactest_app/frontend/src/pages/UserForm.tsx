import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function UserForm() {
  const [formData, setFormData] = useState<any>({ email: '', password_hash: '' });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/user/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/user/${id}`, formData);
    } else {
      await api.post('/user', formData);
    }
    navigate('/user');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} User</h1>
      <form onSubmit={handleSubmit}>
        
        <div>
          <label>Email: </label>
          <input 
            value={formData.email || ''} 
            onChange={e => setFormData({
            ...formData,
            email: e.target.value
          })} 
          />
        </div>
            
        <div>
          <label>Password_Hash: </label>
          <input 
            value={formData.password_hash || ''} 
            onChange={e => setFormData({
            ...formData,
            password_hash: e.target.value
          })} 
          />
        </div>
            
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/user')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
