import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function StudentCourseForm() {
  const [formData, setFormData] = useState<any>({ student_id: '', course_id: '' });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/student_course/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/student_course/${id}`, formData);
    } else {
      await api.post('/student_course', formData);
    }
    navigate('/student_course');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} StudentCourse</h1>
      <form onSubmit={handleSubmit}>
        
        <div>
          <label>Student_Id: </label>
          <input 
            value={formData.student_id || ''} 
            onChange={e => setFormData({
            ...formData,
            student_id: e.target.value
          })} 
          />
        </div>
            
        <div>
          <label>Course_Id: </label>
          <input 
            value={formData.course_id || ''} 
            onChange={e => setFormData({
            ...formData,
            course_id: e.target.value
          })} 
          />
        </div>
            
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/student_course')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
