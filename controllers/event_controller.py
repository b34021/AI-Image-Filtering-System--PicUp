from fastapi import APIRouter, HTTPException
from services.event_service import EventService

router = APIRouter(prefix="/events", tags=["Events"])
event_service = EventService()

@router.post("/")
async def create_event(event_data: dict):
    return await event_service.create_event(event_data)

@router.get("/")
async def get_events():
    return await event_service.list_events()

@router.get("/{event_id}")
async def get_event(event_id: int):
    event = await event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}")
async def update_event(event_id: int, update_data: dict):
    event = await event_service.update_event(event_id, update_data)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/{event_id}")
async def delete_event(event_id: int):
    success = await event_service.remove_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted"}