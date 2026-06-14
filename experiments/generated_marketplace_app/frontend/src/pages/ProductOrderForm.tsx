import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function ProductOrderForm() {
  const [formData, setFormData] = useState<any>({ product_id: '', order_id: '' });
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      api.get(`/product_order/${id}`).then(res => setFormData(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await api.put(`/product_order/${id}`, formData);
    } else {
      await api.post('/product_order', formData);
    }
    navigate('/product_order');
  };

  return (
    <div>
      <h1>{isEdit ? 'Edit' : 'Create'} ProductOrder</h1>
      <form onSubmit={handleSubmit}>
        
        <div>
          <label>Product_Id: </label>
          <input 
            value={formData.product_id || ''} 
            onChange={e => setFormData({
            ...formData,
            product_id: e.target.value
          })} 
          />
        </div>
            
        <div>
          <label>Order_Id: </label>
          <input 
            value={formData.order_id || ''} 
            onChange={e => setFormData({
            ...formData,
            order_id: e.target.value
          })} 
          />
        </div>
            
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/product_order')} style={{ marginLeft: "0.5rem" }}>Cancel</button>
      </form>
    </div>
  );
}
