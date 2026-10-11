import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function PermissionForm() {
  const [formData, setFormData] = useState<any>({ name: '' });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/permission/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/permission/${id}`, formData);
    } else {
      await api.post('/permission', formData);
    }
    navigate('/permission');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} Permission</h1>
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
        <button type="button" onClick={() => navigate('/permission')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
