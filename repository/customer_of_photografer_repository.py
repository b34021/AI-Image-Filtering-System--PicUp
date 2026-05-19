from models.customer_of_photografer import CustomerOfPhotografer

class CustomerOfPhotograferRepository:
    async def create(self, data: dict):
        record = CustomerOfPhotografer(**data)
        await record.insert()
        return record

    async def get(self, record_id: int):
        return await CustomerOfPhotografer.find_one(CustomerOfPhotografer.id == record_id)

    async def get_all(self):
        return await CustomerOfPhotografer.find_all().to_list()

    async def update(self, record_id: int, data: dict):
        record = await CustomerOfPhotografer.find_one(CustomerOfPhotografer.id == record_id)
        if record:
            await record.update({"$set": data})
            return record
        return None

    async def delete(self, record_id: int):
        record = await CustomerOfPhotografer.find_one(CustomerOfPhotografer.id == record_id)
        if record:
            await record.delete()
            return True
        return False