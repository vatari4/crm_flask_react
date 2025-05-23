// src/layouts/MainLayout.jsx
import React from 'react';
import { Layout } from 'antd';
import AppSlider from '../components/AppSlider';
import { Outlet } from 'react-router-dom';

const MainLayout = () => (
  <Layout>
    <AppSlider />
    <Outlet /> {/* сюда будет рендериться AppContent */}
  </Layout>
);

export default MainLayout;
