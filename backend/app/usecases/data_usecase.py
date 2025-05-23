from app.repositories.data_repository import DataRepository

class DataUseCase:
    def __init__(self):
        self.repo = DataRepository()

    def get_analytics_data(self):
        return self.repo.get_analytics()
