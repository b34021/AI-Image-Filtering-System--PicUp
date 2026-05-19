from repository.categorty_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    async def create(self, data: dict):
        return await self.repo.create(data)

    async def list_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, category_id: int):
        return await self.repo.get(category_id)

    async def update(self, category_id: int, data: dict):
        return await self.repo.update(category_id, data)

    async def remove(self, category_id: int):
        return await self.repo.delete(category_id)