// src/routes/AppRouter.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import AppContent from '../components/AppContent';
import PageNotFound from '../pages/PageNotFound';

const AppRouter = () => {
  return (
    <Routes>
      {/* Основной layout */}
      <Route element={<MainLayout />}>
        <Route path="/" element={<AppContent />} />
      </Route>

      {/* Отдельная страница 404 — без MainLayout */}
      <Route path="/404" element={<PageNotFound />} />
      <Route path="*" element={<PageNotFound />} />
    </Routes>
  );
};

export default AppRouter;
