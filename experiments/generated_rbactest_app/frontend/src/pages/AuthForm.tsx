import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function AuthForm() {
  const [formData, setFormData] = useState<any>({  });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/auth/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/auth/${id}`, formData);
    } else {
      await api.post('/auth', formData);
    }
    navigate('/auth');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} Auth</h1>
      <form onSubmit={handleSubmit}>
        
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/auth')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
