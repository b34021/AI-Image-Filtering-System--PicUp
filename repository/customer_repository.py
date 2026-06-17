from models.customer import Customer

class CustomerRepository:
    async def create(self, data: Customer):

        await data.insert()
        return data

    async def get(self, customer_id: str):
        return await Customer.find_one(Customer.id == customer_id)

    async def get_all(self):
        return await Customer.find_all().to_list()

    async def update(self, customer_id: str, data: dict):
        customer = await Customer.find_one(Customer.id == customer_id)
        if customer:
            await customer.update({"$set": data})
            return customer
        return None

    async def delete(self, customer_id: str):
        customer = await Customer.find_one(Customer.id == customer_id)
        if customer:
            await customer.delete()
            return True
        return False