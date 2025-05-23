import React from 'react';
import { Card, Space, Typography } from 'antd';
import { TransactionOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const DealsCard = ({ deals }) => {
  const format = (n) => n?.toLocaleString('ru-RU') || 'N/A';

  return (
    <div style={{ flex: 1 }}>
      <Space align="center" size="middle" style={{ marginBottom: 12 }}>
        <TransactionOutlined style={{ fontSize: 30, color: '#722ed1' }} />
        <Title level={4} style={{ margin: 0 }}>Сделки</Title>
      </Space>
      <Card style={{ width: '100%' }}>
        <Space direction="vertical" size={8}>
          <Text><strong>Всего сделок:</strong> {format(deals.total)}</Text>
          <Text><strong>Завершено:</strong> {format(deals.completed)}</Text>
          <Text><strong>В процессе:</strong> {format(deals.in_progress)}</Text>
          <Text><strong>Средний размер:</strong> {format(deals.avg_deal_size)} ₽</Text>
        </Space>
      </Card>
    </div>
  );
};

export default DealsCard;
