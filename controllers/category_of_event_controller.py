from fastapi import APIRouter, HTTPException
from services.category_of_event_service import CategoryOfEventService

router = APIRouter(prefix="/category_of_events", tags=["CategoryOfEvents"])
service = CategoryOfEventService()

@router.post("/")
async def create_category_of_events(data: dict):
    return await service.create(data)

@router.get("/")
async def get_category_of_events():
    return await service.list_all()

@router.get("/{record_id}")
async def get_category_of_events(record_id: int):
    category_of_events = await service.get_by_id(record_id)
    if not category_of_events:
        raise HTTPException(status_code=404, detail="Record not found")
    return category_of_events

@router.put("/{record_id}")
async def update_record(record_id: int, data: dict):
    category_of_events = await service.update(record_id, data)
    if not category_of_events:
        raise HTTPException(status_code=404, detail="Record not found")
    return category_of_events

@router.delete("/{record_id}")
async def delete_category_of_events(record_id: int):
    success = await service.remove(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted"}