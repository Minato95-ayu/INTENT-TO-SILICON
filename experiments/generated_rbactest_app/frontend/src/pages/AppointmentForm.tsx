import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function AppointmentForm() {
  const [formData, setFormData] = useState<any>({ patient_id: '' });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/appointment/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/appointment/${id}`, formData);
    } else {
      await api.post('/appointment', formData);
    }
    navigate('/appointment');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} Appointment</h1>
      <form onSubmit={handleSubmit}>
        
        <div>
          <label>Patient_Id: </label>
          <input 
            value={formData.patient_id || ''} 
            onChange={e => setFormData({
            ...formData,
            patient_id: e.target.value
          })} 
          />
        </div>
            
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/appointment')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
