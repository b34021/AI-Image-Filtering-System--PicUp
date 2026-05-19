from fastapi import APIRouter, HTTPException
from services.photografer_service import PhotograferService

router = APIRouter(prefix="/photografers", tags=["Photografers"])
service = PhotograferService()

@router.post("/")
async def create_photografer(data: dict):
    return await service.create(data)

@router.get("/")
async def get_photografers():
    return await service.list_all()

@router.get("/{photografer_id}")
async def get_photografer(photografer_id: int):
    photografer = await service.get_by_id(photografer_id)
    if not photografer:
        raise HTTPException(status_code=404, detail="Photografer not found")
    return photografer

@router.put("/{photografer_id}")
async def update_photografer(photografer_id: int, data: dict):
    photografer = await service.update(photografer_id, data)
    if not photografer:
        raise HTTPException(status_code=404, detail="Photografer not found")
    return photografer

@router.delete("/{photografer_id}")
async def delete_photografer(photografer_id: int):
    success = await service.remove(photografer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Photografer not found")
    return {"message": "Photografer deleted"}