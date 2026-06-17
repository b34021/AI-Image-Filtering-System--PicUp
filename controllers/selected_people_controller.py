from fastapi import APIRouter
from dto.selected_people_dto import SelectedPeopleDTO
from services.people_service import save_selected_people

router = APIRouter(prefix="/people", tags=["people"])


@router.post("/")
async def choose_people(dto: SelectedPeopleDTO):
    return await save_selected_people(dto)