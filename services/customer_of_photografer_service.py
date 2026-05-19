from repository.customer_of_photografer_repository import CustomerOfPhotograferRepository

class CustomerOfPhotograferService:
    def __init__(self):
        self.repo = CustomerOfPhotograferRepository()

    async def create(self, data: dict):
        return await self.repo.create(data)

    async def list_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, record_id: int):
        return await self.repo.get(record_id)

    async def update(self, record_id: int, data: dict):
        return await self.repo.update(record_id, data)

    async def remove(self, record_id: int):
        return await self.repo.delete(record_id)