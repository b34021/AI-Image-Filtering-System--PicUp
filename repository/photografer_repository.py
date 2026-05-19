from models.photografer import Photografer

class PhotograferRepository:
    async def create(self, data: dict):
        photografer = Photografer(**data)
        await photografer.insert()
        return photografer

    async def get(self, photografer_id: int):
        return await Photografer.find_one(Photografer.id == photografer_id)

    async def get_all(self):
        return await Photografer.find_all().to_list()

    async def update(self, photografer_id: int, data: dict):
        photografer = await Photografer.find_one(Photografer.id == photografer_id)
        if photografer:
            await photografer.update({"$set": data})
            return photografer
        return None

    async def delete(self, photografer_id: int):
        photografer = await Photografer.find_one(Photografer.id == photografer_id)
        if photografer:
            await photografer.delete()
            return True
        return False