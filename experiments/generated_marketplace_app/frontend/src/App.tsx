import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import OrderList from './pages/OrderList';
import OrderForm from './pages/OrderForm';
import ProductList from './pages/ProductList';
import ProductForm from './pages/ProductForm';
import ProductOrderList from './pages/ProductOrderList';
import ProductOrderForm from './pages/ProductOrderForm';

export default function App() {
  return (
    <Router>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <strong>Aayu App</strong> | <Link to='/order'>Order</Link> | <Link to='/product'>Product</Link> | <Link to='/product_order'>ProductOrder</Link> 
      </nav>
      <div style={{ padding: '1rem' }}>
        <Routes>
          <Route path='/' element={<h2>Welcome to Aayu Generated App</h2>} />
          <Route path='/order' element={<OrderList />} />
          <Route path='/order/new' element={<OrderForm />} />
          <Route path='/order/edit/:id' element={<OrderForm />} />
          <Route path='/product' element={<ProductList />} />
          <Route path='/product/new' element={<ProductForm />} />
          <Route path='/product/edit/:id' element={<ProductForm />} />
          <Route path='/product_order' element={<ProductOrderList />} />
          <Route path='/product_order/new' element={<ProductOrderForm />} />
          <Route path='/product_order/edit/:id' element={<ProductOrderForm />} />
        </Routes>
      </div>
    </Router>
  );
}
