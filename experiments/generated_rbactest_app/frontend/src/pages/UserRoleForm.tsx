import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function UserRoleForm() {
  const [formData, setFormData] = useState<any>({ user_id: '', role_id: '' });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/user_role/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/user_role/${id}`, formData);
    } else {
      await api.post('/user_role', formData);
    }
    navigate('/user_role');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} UserRole</h1>
      <form onSubmit={handleSubmit}>
        
        <div>
          <label>User_Id: </label>
          <input 
            value={formData.user_id || ''} 
            onChange={e => setFormData({
            ...formData,
            user_id: e.target.value
          })} 
          />
        </div>
            
        <div>
          <label>Role_Id: </label>
          <input 
            value={formData.role_id || ''} 
            onChange={e => setFormData({
            ...formData,
            role_id: e.target.value
          })} 
          />
        </div>
            
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/user_role')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
