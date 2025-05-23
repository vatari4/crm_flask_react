import React from 'react';
import { Card, Space, Typography } from 'antd';

const { Text } = Typography;

const TopEmployeeCard = ({ topEmployee, teamAverage }) => {
  const format = (n) => n?.toLocaleString('ru-RU') || 'N/A';

  return (
    <Card
      title="Лучший сотрудник"
      headStyle={{ backgroundColor: '#fa8c16', color: 'white' }}
      style={{ width: 480, flexShrink: 0 }}
    >
      <Space direction="vertical" size="middle">
        <div>
          <Text strong>Имя: </Text>
          <Text>{topEmployee.name}</Text>
        </div>
        <div>
          <Text strong>Отдел: </Text>
          <Text>{topEmployee.department}</Text>
        </div>
        <div>
          <Text strong>KPI: </Text>
          <Text type={topEmployee.kpi > 1 ? 'success' : 'warning'}>
            {topEmployee.kpi}
          </Text>
        </div>
        <div>
          <Text strong>Закрытые сделки: </Text>
          <Text>{topEmployee.deals_closed}</Text>
        </div>
        <div>
          <Text strong>Выручка: </Text>
          <Text type="success">{format(topEmployee.revenue_generated)} ₽</Text>
        </div>
        <div>
          <Text strong>Средний KPI команды: </Text>
          <Text>{teamAverage}</Text>
        </div>
      </Space>
    </Card>
  );
};

export default TopEmployeeCard;
