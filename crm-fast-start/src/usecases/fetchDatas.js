// usecases/fetchDatas.js
const fetchDatas = async (userId) => {
  const response = await fetch(`http://localhost:5000/api/data?userid=${userId}`);
  if (!response.ok) {
    throw new Error(`Ошибка загрузки данных: ${response.status}`);
  }
  return await response.json();
};

export default fetchDatas;
