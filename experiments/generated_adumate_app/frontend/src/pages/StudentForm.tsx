import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function StudentForm() {
  const [formData, setFormData] = useState<any>({  });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/student/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/student/${id}`, formData);
    } else {
      await api.post('/student', formData);
    }
    navigate('/student');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} Student</h1>
      <form onSubmit={handleSubmit}>
        
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/student')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
