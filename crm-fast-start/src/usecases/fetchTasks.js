const fetchTasks = async (userId) => {
  const response = await fetch(`http://localhost:5000/api/tasks?userid=${userId}`);
  if (!response.ok) {
    throw new Error(`Ошибка загрузки задач: ${response.status}`);
  }
  const data = await response.json();
  return data; // возвращаем весь объект с tasks и metadata
};

export default fetchTasks;
