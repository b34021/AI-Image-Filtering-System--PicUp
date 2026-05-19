from models.categories_of_event import CategoryOfEvent

class CategoryOfEventRepository:
    async def create(self, data: dict):
        record = CategoryOfEvent(**data)
        await record.insert()
        return record

    async def get(self, record_id: int):
        return await CategoryOfEvent.find_one(CategoryOfEvent.id == record_id)

    async def get_all(self):
        return await CategoryOfEvent.find_all().to_list()

    async def update(self, record_id: int, data: dict):
        record = await CategoryOfEvent.find_one(CategoryOfEvent.id == record_id)
        if record:
            await record.update({"$set": data})
            return record
        return None

    async def delete(self, record_id: int):
        record = await CategoryOfEvent.find_one(CategoryOfEvent.id == record_id)
        if record:
            await record.delete()
            return True
        return False