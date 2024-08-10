import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Chatbot from '@/components/Chatbot';
import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Chatbot />
  </StrictMode>,
)
