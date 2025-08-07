# app/simulation/simulation_service.py
from datetime import datetime, timedelta
import random
import numpy as np
from app.models import db
from app.models.task import Task

class SimulationService:
    @staticmethod
    def simulate_client_requests(user_id, params):
        """
        Реализация метода имитационного моделирования из работы.
        Параметры:
        - user_id: ID пользователя
        - params: {
            "time_period": 7,       # дней для симуляции
            "request_intensity": 50 # среднее количество запросов в день
          }
        """
        # Очистка предыдущих симуляций
        Task.query.filter_by(user_id=user_id, is_simulated=True).delete()
        
        tasks = []
        base_date = datetime.now()
        
        # Применяем пуассоновский поток запросов (как в статье)
        for day in range(params["time_period"]):
            date = base_date - timedelta(days=day)
            requests_count = np.random.poisson(params["request_intensity"])
            
            for _ in range(requests_count):
                # Генерация задачи с учетом приоритетов
                processing_time = random.expovariate(1/30)  # Экспоненциальное распределение
                
                task = Task(
                    title=f"Client request #{random.randint(1000,9999)}",
                    due_date=date + timedelta(minutes=random.randint(1, 1440)),
                    status="new",
                    priority=self._calculate_priority(processing_time),
                    user_id=user_id,
                    is_simulated=True,
                    processing_time=processing_time
                )
                tasks.append(task)
                db.session.add(task)
        
        db.session.commit()
        return tasks

    @staticmethod
    def _calculate_priority(processing_time):
        """Определение приоритета на основе времени обработки"""
        if processing_time > 45:
            return "low"
        elif processing_time > 20:
            return "medium"
        return "high"