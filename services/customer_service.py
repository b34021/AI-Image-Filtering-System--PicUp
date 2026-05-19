from repository.customer_repository import CustomerRepository

class CustomerService:
    def __init__(self):
        self.repo = CustomerRepository()

    async def create(self, data: dict):
        return await self.repo.create(data)

    async def list_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, customer_id: int):
        return await self.repo.get(customer_id)

    async def update(self, customer_id: int, data: dict):
        return await self.repo.update(customer_id, data)

    async def remove(self, customer_id: int):
        return await self.repo.delete(customer_id)