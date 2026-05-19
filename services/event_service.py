from repository.event_repository import EventRepository

class EventService:
    def __init__(self):
        self.repo = EventRepository()

    async def create_event(self, event_data: dict):
        # כאן ניתן להוסיף לוגיקה נוספת לפני השמירה
        return await self.repo.create_event(event_data)

    async def list_events(self):
        return await self.repo.get_all_events()

    async def get_event_by_id(self, event_id: int):
        return await self.repo.get_event(event_id)

    async def update_event(self, event_id: int, update_data: dict):
        return await self.repo.update_event(event_id, update_data)

    async def remove_event(self, event_id: int):
        return await self.repo.delete_event(event_id)