from fastapi import APIRouter, HTTPException
from services.category_of_event_service import CategoryOfEventService

router = APIRouter(prefix="/category_of_events", tags=["CategoryOfEvents"])
service = CategoryOfEventService()

@router.post("/")
async def create_record(data: dict):
    return await service.create(data)

@router.get("/")
async def get_records():
    return await service.list_all()

@router.get("/{record_id}")
async def get_record(record_id: int):
    record = await service.get_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/{record_id}")
async def update_record(record_id: int, data: dict):
    record = await service.update(record_id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.delete("/{record_id}")
async def delete_record(record_id: int):
    success = await service.remove(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted"}