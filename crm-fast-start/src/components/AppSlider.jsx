import React from 'react';
import { Layout, Menu } from 'antd';
import {
  AppstoreOutlined,
  BarChartOutlined,
  CloudOutlined,
  ShopOutlined,
  TeamOutlined,
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons';

const { Sider } = Layout;

const siderStyle = {
  overflow: 'auto',
  height: '100vh',
  position: 'fixed',
  left: 0,
  top: 0,
  bottom: 0,
};

const items = [
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  BarChartOutlined,
  CloudOutlined,
  AppstoreOutlined,
  TeamOutlined,
  ShopOutlined,
].map((icon, index) => ({
  key: String(index + 1),
  icon: React.createElement(icon),
  label: `nav ${index + 1}`,
}));

const AppSlider = () => {
  return (
    <Sider style={siderStyle} width={280}>
      <div className="demo-logo-vertical" />
      <Menu 
        theme="dark" 
        mode="inline" 
        defaultSelectedKeys={['4']} 
        items={items} 
      />
    </Sider>
  );
};

export default AppSlider;