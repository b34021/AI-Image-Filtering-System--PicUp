from beanie import Document

class CategoryOfEvent(Document):
    id: int
    categoriesId: int
    eventId: int
    precentQuentity: str

    class Settings:
        name = "categories_of_event"