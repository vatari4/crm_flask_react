import React, { useEffect, useState } from 'react';
import { Layout, Space, Card, Spin, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';

import UsersCard from '../components/UsersCard';
import ContractsCard from '../components/ContractsCard';
import DealsCard from '../components/DealsCard';
import TopEmployeeCard from '../components/TopEmployeeCard';

import fetchDatas from '../usecases/fetchDatas';
import fetchTasks from '../usecases/fetchTasks';

import TasksModal from '../components/TasksModal';

const { Content } = Layout;
const { Title, Text } = Typography;
const SIDEBAR_WIDTH = 280;

const AppContent = () => {
  const [data, setData] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isTasksModalVisible, setIsTasksModalVisible] = useState(false);

  const navigate = useNavigate();
  const userId = 123;

  useEffect(() => {
    const loadData = async () => {
      try {
        const result = await fetchDatas(userId);
        setData(result);
      } catch (err) {
        setError(err.message);
        console.error('Ошибка при загрузке данных:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
    const intervalId = setInterval(loadData, 30000);
    return () => clearInterval(intervalId);
  }, [userId]);

  useEffect(() => {
    const loadTasks = async () => {
      try {
        const response = await fetchTasks(userId);
        const tasksArray = response.tasks || response;
        setTasks(tasksArray);

        if (tasksArray.length > 0) {
          setIsTasksModalVisible(true);
        }
      } catch (err) {
        console.error('Ошибка при загрузке задач:', err);
      }
    };

    loadTasks();
  }, [userId]);

  // Закрытие модалки, если задач больше нет
  useEffect(() => {
    if (isTasksModalVisible && tasks.length === 0) {
      setIsTasksModalVisible(false);
    }
  }, [tasks, isTasksModalVisible]);

  const formatNumber = (num) => num?.toLocaleString('ru-RU') || 'N/A';

  if (loading) {
    return (
      <Layout style={{ marginLeft: SIDEBAR_WIDTH }}>
        <Content
          style={{
            margin: '20px',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '80vh',
          }}
        >
          <Spin tip="Загрузка данных..." size="large" />
        </Content>
      </Layout>
    );
  }

  if (error || !data) {
    navigate('/404');
    return null;
  }

  return (
    <Layout style={{ marginLeft: SIDEBAR_WIDTH }}>
      <Content style={{ margin: '24px' }}>
        <Space direction="vertical" size={20} style={{ width: '100%' }}>
          <div style={{ display: 'flex', gap: '20px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', flex: 1 }}>
              <Card title="Новые пользователи" headStyle={{ backgroundColor: '#1890ff', color: 'white' }} style={{ height: 160 }}>
                <Text strong style={{ fontSize: 20 }}>
                  {formatNumber(data.analytics.users.new_visitors)}
                </Text>
              </Card>

              <Card title="Контракты в процессе" headStyle={{ backgroundColor: '#52c41a', color: 'white' }} style={{ height: 160 }}>
                <Text strong style={{ fontSize: 20 }}>
                  {formatNumber(data.analytics.contracts.in_progress)}
                </Text>
              </Card>

              <Card title="Завершённые сделки" headStyle={{ backgroundColor: '#722ed1', color: 'white' }} style={{ height: 160 }}>
                <Text strong style={{ fontSize: 20 }}>
                  {formatNumber(data.analytics.deals.completed)}
                </Text>
              </Card>
            </div>

            <TopEmployeeCard
              topEmployee={data.analytics.performance.top_employee}
              teamAverage={data.analytics.performance.team_average}
            />
          </div>

          <Title level={4}>Пользователи</Title>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 32 }}>
            <UsersCard users={data.analytics.users} />
            <ContractsCard contracts={data.analytics.contracts} />
            <DealsCard deals={data.analytics.deals} />
          </div>

          <TasksModal
            open={isTasksModalVisible}
            onCancel={() => setIsTasksModalVisible(false)}
            tasks={tasks}
            setTasks={setTasks}
          />
        </Space>
      </Content>
    </Layout>
  );
};

export default AppContent;
