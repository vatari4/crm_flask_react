import React from 'react';
import { Card, Space, Typography } from 'antd';
import { UserOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const UsersCard = ({ users }) => {
  const format = (n) => n?.toLocaleString('ru-RU') || 'N/A';

  return (
    <div style={{ flex: 1, marginRight: 16 }}>
      <Space align="center" size="middle" style={{ marginBottom: 12 }}>
        <UserOutlined style={{ fontSize: 30, color: '#1890ff' }} />
        <Title level={4} style={{ margin: 0 }}>Пользователи</Title>
      </Space>
      <Card style={{ width: '100%' }}>
        <Space direction="vertical" size={8}>
          <Text><strong>Всего посетителей:</strong> {format(users.total_visitors)}</Text>
          <Text><strong>Новых:</strong> {format(users.new_visitors)}</Text>
          <Text><strong>Возвратившихся:</strong> {format(users.returning_visitors)}</Text>
        </Space>
      </Card>
    </div>
  );
};

export default UsersCard;
