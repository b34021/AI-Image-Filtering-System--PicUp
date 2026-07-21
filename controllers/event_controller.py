import json
import os
import asyncio
from fastapi import APIRouter, HTTPException
from services.event_service import EventService
from dto.EventDTO import EventDTO
from services.face_selected import FaceSelectedService
from services.deduplicate import DeduplicateService
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from fastapi.responses import JSONResponse
from dto.folderRequest import FolderRequest


router = APIRouter(prefix="/event", tags=["Events"])

service = FaceSelectedService()
event_service = EventService()
deduplicate_service = DeduplicateService()


@router.post("/get_faces")
async def get_faces(event_data: EventDTO):
    return await event_service.get_faces(event_data)

@router.post("/")
async def create_event(event_data: EventDTO):
    """יצירת אירוע + בניית אלבום — מסיר כפילויות, מנקד, מפיץ לקטגוריות."""
    try:
        result = await event_service.build_album(event_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-images")
async def get_images(data: FolderRequest):
    folder = Path(data.path)

    if not folder.exists():
        raise HTTPException(status_code=404, detail="Folder does not exist")

    if not folder.is_dir():
        raise HTTPException(status_code=400, detail="Path is not a directory")

    images = await event_service.get_images_as_base64(str(folder))
    return images



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
async def update_event(event_id: str, update_data: dict):
    event = await event_service.update_event(event_id, update_data)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.delete("/{event_id}")
async def delete_event(event_id: str):
    success = await event_service.remove_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted"}



IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}
@router.post("/count-images")
async def count_images(data:FolderRequest):
    folder = Path(data.path)

    if not folder.exists():
        return {"error": "Folder does not exist"}

    if not folder.is_dir():
        return {"error": "Path is not a directory"}

    image_count = sum(
        1
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )

    return {"image_count": image_count}


@router.post("/select-folder")
def select_folder():
    global selected_folder

    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', True)

    folder = filedialog.askdirectory(title="בחר תיקייה עם תמונות")
    root.destroy()

    if not folder:
        return JSONResponse(content={"success": False})

    selected_folder = folder
    return JSONResponse(content={"success": True, "path": folder})
