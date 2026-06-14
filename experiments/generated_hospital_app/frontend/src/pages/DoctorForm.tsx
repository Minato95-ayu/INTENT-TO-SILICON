import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function DoctorForm() {
  const [formData, setFormData] = useState<any>({  });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/doctor/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/doctor/${id}`, formData);
    } else {
      await api.post('/doctor', formData);
    }
    navigate('/doctor');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} Doctor</h1>
      <form onSubmit={handleSubmit}>
        
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/doctor')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
