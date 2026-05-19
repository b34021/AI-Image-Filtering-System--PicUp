from models.Category import Category

class CategoryRepository:
    async def create(self, data: dict):
        category = Category(**data)
        await category.insert()
        return category

    async def get(self, category_id: int):
        return await Category.find_one(Category.id == category_id)

    async def get_all(self):
        return await Category.find_all().to_list()

    async def update(self, category_id: int, data: dict):
        category = await Category.find_one(Category.id == category_id)
        if category:
            await category.update({"$set": data})
            return category
        return None

    async def delete(self, category_id: int):
        category = await Category.find_one(Category.id == category_id)
        if category:
            await category.delete()
            return True
        return False