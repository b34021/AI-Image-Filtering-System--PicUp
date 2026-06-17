from fastapi import APIRouter, HTTPException

from controllers.event_controller import event_service
from services.build import Build
router = APIRouter(prefix="/customers", tags=["Customers"])
service = Build(eventid=1)
"""
מקבל id ארוע,לקוח

"""

@router.get("/{event_id}")
async def get_event(event_id: int):
    event = await event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/{customer_id}")
async def get_customer(customer_id: str):
    customer = await service.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/{customer_id}")
async def get_Book(custid: int,eventid: int):
    book = await service.Build(custid,eventid)
    if not book:
        raise HTTPException(status_code=404, detail="Customer not found")
    return book


