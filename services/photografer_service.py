from repository.photografer_repository import PhotograferRepository

class PhotograferService:
    def __init__(self):
        self.repo = PhotograferRepository()

    async def create(self, data: dict):
        return await self.repo.create(data)

    async def list_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, photografer_id: int):
        return await self.repo.get(photografer_id)

    async def update(self, photografer_id: int, data: dict):
        return await self.repo.update(photografer_id, data)

    async def remove(self, photografer_id: int):
        return await self.repo.delete(photografer_id)