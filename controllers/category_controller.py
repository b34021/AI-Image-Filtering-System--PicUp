from fastapi import APIRouter, HTTPException
from services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])
service = CategoryService()

@router.post("/")
async def create_category(data: dict):
    return await service.create(data)

@router.get("/")
async def get_categories():
    return await service.list_all()

@router.get("/{category_id}")
async def get_category(category_id: int):
    category = await service.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}")
async def update_category(category_id: int, data: dict):
    category = await service.update(category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}")
async def delete_category(category_id: int):
    success = await service.remove(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}