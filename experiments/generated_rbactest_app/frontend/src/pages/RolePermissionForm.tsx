import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function RolePermissionForm() {
  const [formData, setFormData] = useState<any>({ role_id: '', permission_id: '' });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/role_permission/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/role_permission/${id}`, formData);
    } else {
      await api.post('/role_permission', formData);
    }
    navigate('/role_permission');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} RolePermission</h1>
      <form onSubmit={handleSubmit}>
        
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
            
        <div>
          <label>Permission_Id: </label>
          <input 
            value={formData.permission_id || ''} 
            onChange={e => setFormData({
            ...formData,
            permission_id: e.target.value
          })} 
          />
        </div>
            
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/role_permission')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
