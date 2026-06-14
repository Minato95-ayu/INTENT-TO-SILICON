import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import OrderList from './pages/OrderList';
import OrderForm from './pages/OrderForm';
import ProductList from './pages/ProductList';
import ProductForm from './pages/ProductForm';
import ProductOrderList from './pages/ProductOrderList';
import ProductOrderForm from './pages/ProductOrderForm';

function Home() {
  return (
    <div>
      <h1>Aayu Generated Dashboard</h1>
      <p>Welcome to your full-stack application.</p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: '1rem', background: '#f0f0f0', marginBottom: '2rem' }}>
        <Link to="/" style={{marginRight: "2rem", fontWeight: "bold"}}>Home</Link>
        <Link to="/order" style={{marginRight: "1rem"}}>Order</Link>
        <Link to="/product" style={{marginRight: "1rem"}}>Product</Link>
        <Link to="/product_order" style={{marginRight: "1rem"}}>Product Order</Link>
      </nav>
      <div style={{ padding: '0 2rem' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/order" element={<OrderList />} />
          <Route path="/order/new" element={<OrderForm />} />
          <Route path="/order/edit/:id" element={<OrderForm />} />
          <Route path="/product" element={<ProductList />} />
          <Route path="/product/new" element={<ProductForm />} />
          <Route path="/product/edit/:id" element={<ProductForm />} />
          <Route path="/product_order" element={<ProductOrderList />} />
          <Route path="/product_order/new" element={<ProductOrderForm />} />
          <Route path="/product_order/edit/:id" element={<ProductOrderForm />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
