from app.repositories.counterparty_repository import CounterpartyRepository

class CounterpartyUseCase:
    def __init__(self, repository: CounterpartyRepository):
        self.repo = repository

    def list_counterparties(self):
        return self.repo.get_all()

    def get_counterparty(self, counterparty_id):
        return self.repo.get_by_id(counterparty_id)

    def create_counterparty(self, data):
        if self.repo.get_by_inn(data.get('inn')):
            return None, "Контрагент с таким ИНН уже существует"
        return self.repo.create(data), None

    def update_counterparty(self, counterparty_id, data):
        counterparty = self.repo.get_by_id(counterparty_id)
        if not counterparty:
            return None, "Контрагент не найден"
        return self.repo.update(counterparty, data), None

    def delete_counterparty(self, counterparty_id):
        counterparty = self.repo.get_by_id(counterparty_id)
        if not counterparty:
            return False
        self.repo.delete(counterparty)
        return True