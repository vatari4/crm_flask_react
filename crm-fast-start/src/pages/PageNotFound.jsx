import React from 'react';
import { Button, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';
import {
  MailOutlined,
  PhoneOutlined,
} from '@ant-design/icons';
import {
  FaTelegramPlane,
  FaVk,
  FaWhatsapp,
} from 'react-icons/fa';

import backgroundImage from '../assets/images/sawa.png';

const { Text } = Typography;
const FOOTER_HEIGHT = 100;

const PageNotFound = () => {
  const navigate = useNavigate();

  return (
    <div style={{
      height: '100vh',
      width: '100vw',
      background: 'linear-gradient(135deg, #1c1c1c, #000)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      overflow: 'hidden',
    }}>
      {/* Основной контент */}
      <div style={{
        display: 'flex',
        flex: 1,
        padding: '40px',
        boxSizing: 'border-box',
      }}>
        {/* Остров */}
        <div style={{
          width: '70%',
          backgroundColor: 'rgba(255, 255, 255, 0.07)',
          backdropFilter: 'blur(20px)',
          borderRadius: '24px',
          padding: '80px',
          position: 'relative',
          boxShadow: '0 10px 40px rgba(0,0,0,0.6)',
          animation: 'slideInIsland 1s ease-out forwards',
          transform: 'translateX(-100%)',
          opacity: 0,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
        }}>
          {/* 404 фон на острове */}
          <h1 style={{
            position: 'absolute',
            bottom: FOOTER_HEIGHT + 20,
            left: '40px',
            fontSize: 'calc(70vh * 0.7)',
            fontWeight: 900,
            color: '#ffffff09',
            zIndex: 0,
            lineHeight: 1,
            margin: 0,
            pointerEvents: 'none',
          }}>404</h1>

          <div style={{ position: 'relative', zIndex: 1 }}>
            <h1 style={{
              fontSize: 100,
              color: '#fff',
              marginBottom: 20,
              lineHeight: 1,
              fontWeight: 900,
            }}>ОШИБКА</h1>

            <p style={{
              fontSize: 40,
              color: '#ddd',
              marginBottom: 32,
              fontWeight: 500,
            }}>
              Страница не найдена
            </p>

            <p style={{
              fontSize: 20,
              color: '#bbb',
              marginBottom: 60,
              maxWidth: '80%',
            }}>
              Пожалуйста, перезапустите чуть позже или свяжитесь с нашей командой поддержки.
            </p>

            <Button type="primary" size="large" onClick={() => navigate('/')}>
              Вернуться на главную
            </Button>
          </div>
        </div>

        {/* Правая зона с фото */}
        <div style={{
          width: '30%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 20,
          marginLeft: 20,
        }}>
          <div style={{
            flex: 1,
            width: '100%',
            borderRadius: '24px',
            overflow: 'hidden',
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            animation: 'slideInImage 1.4s ease-out forwards',
            animationDelay: '2s',
            transform: 'translateX(100%)',
            opacity: 0,
          }} />
          
          <Text style={{
            color: '#fff',
            fontSize: 18,
            textAlign: 'center',
            fontStyle: 'italic',
            animation: 'fadeIn 2s ease forwards',
            animationDelay: '3s',
            opacity: 0,
          }}>
            "Эй, баля, у меня всё работает!"
          </Text>
        </div>
      </div>

      {/* Футер */}
      <div style={{
        height: `${FOOTER_HEIGHT}px`,
        width: '100%',
        padding: '0 40px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        color: '#ccc',
        backgroundColor: 'rgba(0,0,0,0.6)',
        borderTop: '1px solid rgba(255,255,255,0.1)',
        animation: 'fadeInUp 1.5s ease forwards',
        opacity: 0,
      }}>
        {/* Лево */}
        <div style={{ fontWeight: 'bold', fontSize: 24 }}>
          FASTSTART
        </div>

        {/* Центр */}
        <div style={{ display: 'flex', gap: 32, fontSize: 28 }}>
          <a href="https://t.me/yourtelegram" target="_blank" rel="noopener noreferrer" style={{ color: '#ccc' }}>
            <FaTelegramPlane />
          </a>
          <a href="https://vk.com/yourvk" target="_blank" rel="noopener noreferrer" style={{ color: '#ccc' }}>
            <FaVk />
          </a>
          <a href="mailto:support@example.com" style={{ color: '#ccc' }}>
            <MailOutlined />
          </a>
          <a href="https://wa.me/79161234567" target="_blank" rel="noopener noreferrer" style={{ color: '#ccc' }}>
            <FaWhatsapp />
          </a>
        </div>

        {/* Право */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <PhoneOutlined />
          <span>+7 (916) 123-45-67</span>
        </div>
      </div>

      {/* Анимации */}
      <style>{`
        @keyframes slideInIsland {
          0% {
            transform: translateX(-100%);
            opacity: 0;
          }
          100% {
            transform: translateX(0);
            opacity: 1;
          }
        }

        @keyframes slideInImage {
          0% {
            transform: translateX(100%);
            opacity: 0;
          }
          100% {
            transform: translateX(0);
            opacity: 1;
          }
        }

        @keyframes fadeInUp {
          0% {
            transform: translateY(100%);
            opacity: 0;
          }
          100% {
            transform: translateY(0);
            opacity: 1;
          }
        }

        @keyframes fadeIn {
          0% { opacity: 0; }
          100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default PageNotFound;