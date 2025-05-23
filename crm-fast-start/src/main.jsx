import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import AppSlider from './components/AppSlider'

createRoot(document.getElementById('root')).render(
    <App />
)
