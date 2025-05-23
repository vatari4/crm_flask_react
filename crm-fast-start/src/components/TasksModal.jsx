import React, { useState } from 'react';
import { Modal, Card, Typography, Tag, Row, Col, Button } from 'antd';
import { CheckOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useSwipeable } from 'react-swipeable';
import ModalImages from '../assets/images/sawa-modal.jpg';
const { Text } = Typography;

const priorityColors = {
  Высокий: { tag: 'red' },
  Средний: { tag: 'orange' },
  Низкий: { tag: 'green' },
};

const TaskCard = ({ task, onRemove }) => {
  const navigate = useNavigate();
  const [isRemoving, setIsRemoving] = useState(false);
  const [removeDirection, setRemoveDirection] = useState(null);

  const handleRemove = (direction = 'left') => {
    setRemoveDirection(direction);
    setIsRemoving(true);
    setTimeout(() => {
      onRemove(task.id);
    }, 300);
  };

  const handlers = useSwipeable({
    onSwipedLeft: () => handleRemove('left'),
    onSwipedRight: () => handleRemove('right'),
    preventDefaultTouchmoveEvent: true,
    trackMouse: true,
  });

  const tagColor = priorityColors[task.priority]?.tag || 'default';

  return (
    <Col
      span={12}
      {...handlers}
      style={{
        transition: 'transform 0.3s ease, opacity 0.3s ease',
        transform: isRemoving
          ? removeDirection === 'right'
            ? 'translateX(100%)'
            : 'translateX(-100%)'
          : 'translateX(0)',
        opacity: isRemoving ? 0 : 1,
      }}
    >
      <Card
        title={task.title}
        bordered={false}
        style={{
          backgroundColor: '#f5f5f5',
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          cursor: 'pointer',
          userSelect: 'none',
        }}
        headStyle={{
          backgroundColor: '#d9d9d9',
          borderTopLeftRadius: 12,
          borderTopRightRadius: 12,
        }}
        bodyStyle={{ paddingBottom: 12 }}
        onDoubleClick={() => navigate(`/tasks&id=${task.id}`)}
      >
        <p><Text strong>Ответственный:</Text> {task.assignee}</p>
        <p><Text strong>Срок:</Text> {task.due_date}</p>
        <p><Text strong>Статус:</Text> <Tag color="blue">{task.status}</Tag></p>
        <p><Text strong>Приоритет:</Text> <Tag color={tagColor}>{task.priority}</Tag></p>
<img
          src= {ModalImages} // Можно заменить на свою фотографию
          alt="User"
        />
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginTop: 16,
          }}
        >
          <Button
            type="primary"
            icon={<CheckOutlined />}
            onClick={() => handleRemove('left')}
            style={{
              backgroundColor: '#52c41a',
              borderColor: '#52c41a',
              borderRadius: 6,
            }}
          >
            Принять
          </Button>

          <Button
            icon={<InfoCircleOutlined />}
            onClick={() => navigate(`/tasks&id=${task.id}`)}
          >
            Подробнее
          </Button>
        </div>
      </Card>
    </Col>
  );
};

const TasksModal = ({ open, onCancel, tasks, setTasks }) => {
  const removeTask = (taskId) => {
    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  };

  return (
    <Modal
      title="Список задач"
      open={open}
      onCancel={onCancel}
      footer={null}
      width={900}
      centered
      bodyStyle={{ padding: '24px 32px', position: 'relative' }} // добавили relative для позиционирования фото
    >
      {tasks?.length > 0 ? (
        <Row gutter={[20, 20]}>
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} onRemove={removeTask} />
          ))}
        </Row>
      ) : (
        <Text>Нет задач для отображения</Text>
      )}

      {/* Фото внизу справа */}
      <div
        style={{
          position: 'absolute',
          bottom: 16,
          right: 16,
          overflow: 'hidden',
          boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
          border: '2px solid #fff',
          backgroundColor: '#fff',
        }}
      >
        
      </div>
    </Modal>
  );
};

export default TasksModal;
