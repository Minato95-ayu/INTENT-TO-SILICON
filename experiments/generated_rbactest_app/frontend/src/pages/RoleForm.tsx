import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function RoleForm() {
  const [formData, setFormData] = useState<any>({ name: '' });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/role/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/role/${id}`, formData);
    } else {
      await api.post('/role', formData);
    }
    navigate('/role');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} Role</h1>
      <form onSubmit={handleSubmit}>
        
        <div>
          <label>Name: </label>
          <input 
            value={formData.name || ''} 
            onChange={e => setFormData({
            ...formData,
            name: e.target.value
          })} 
          />
        </div>
            
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/role')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
