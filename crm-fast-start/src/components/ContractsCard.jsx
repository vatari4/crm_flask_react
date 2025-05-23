import React from 'react';
import { Card, Space, Typography } from 'antd';
import { FileProtectOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const ContractsCard = ({ contracts }) => {
  const format = (n) => n?.toLocaleString('ru-RU') || 'N/A';

  return (
    <div style={{ flex: 1, marginRight: 16 }}>
      <Space align="center" size="middle" style={{ marginBottom: 12 }}>
        <FileProtectOutlined style={{ fontSize: 30, color: '#52c41a' }} />
        <Title level={4} style={{ margin: 0 }}>Контракты</Title>
      </Space>
      <Card style={{ width: '100%' }}>
        <Space direction="vertical" size={8}>
          <Text><strong>Всего контрактов:</strong> {format(contracts.total)}</Text>
          <Text><strong>В процессе:</strong> {format(contracts.in_progress)}</Text>
          <Text><strong>Подписано:</strong> {format(contracts.signed)}</Text>
          <Text><strong>Отклонено:</strong> {format(contracts.rejected)}</Text>
        </Space>
      </Card>
    </div>
  );
};

export default ContractsCard;
